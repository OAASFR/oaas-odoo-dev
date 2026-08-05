import base64
import datetime
import html

import odoo
import json
import openpyxl
from PIL import Image as PILImage
from odoo.http import request
from odoo.tools import json

HOST = 'localhost'
PORT = 5432  # Port par défaut d'Odoo
DATABASE = 'oaas'
USERNAME = 'odoo'
PASSWORD = 'odoo'
URI = 'postgresql://%s:%s@%s:%d/%s' % (USERNAME, PASSWORD, HOST, PORT, DATABASE)


# Largeur max (px) des images stockees : au-dela on redimensionne. 1920px
# couvre largement un affichage full-width sur grand ecran tout en evitant de
# stocker des images de plusieurs dizaines de Mpx (lourdeur base + site).
MAX_IMAGE_WIDTH = 1920


def _resized_image_bytes(stream):
	# Redimensionne l'image si elle depasse MAX_IMAGE_WIDTH, en conservant le
	# ratio et le format d'origine. Retourne (octets, format_pil) ; en cas
	# d'echec (format non gere par PIL, etc.) on retombe sur l'image d'origine.
	try:
		import io
		img = PILImage.open(io.BytesIO(stream))
		fmt = img.format  # 'PNG', 'JPEG', ...
		if img.width <= MAX_IMAGE_WIDTH:
			return stream, fmt
		ratio = MAX_IMAGE_WIDTH / float(img.width)
		new_size = (MAX_IMAGE_WIDTH, max(1, int(img.height * ratio)))
		img = img.resize(new_size, PILImage.LANCZOS)
		buf = io.BytesIO()
		img.save(buf, format=fmt)
		return buf.getvalue(), fmt
	except Exception:
		return stream, None


def add_attachment_file(file, record, i, col_start):
	attachments = record.env['ir.attachment']
	stream = file.ref.getvalue()
	stream, _fmt = _resized_image_bytes(stream)
	file_data_base64 = base64.b64encode(stream).decode('ascii')
	attachment_id = attachments.sudo().create({
		'name': str(record.id) + "_" + str(i) + "_" + str(col_start) + "." + file.format,
		'datas': file_data_base64,
		'res_model': 'blog.post',
		'res_id': 0,
		'public': True
	})
	return attachment_id


def _split_heading(text):
	# Separe l'accroche (1er <h3>...</h3> en tete de cellule) du reste du texte.
	# L'accroche devient le grand titre bleu de la section ; le reste est le
	# corps. Retourne (accroche_html_interieur, reste). Si pas de <h3> en tete,
	# accroche vide et tout le texte en corps.
	import re
	if not isinstance(text, str):
		return '', ''
	m = re.match(r'\s*<h3[^>]*>(.*?)</h3>\s*', text, flags=re.IGNORECASE | re.DOTALL)
	if not m:
		return '', text
	return m.group(1).strip(), text[m.end():]


def _space_paragraphs(html_text):
	# Ajoute des marges verticales (classes Bootstrap) aux blocs du corps de
	# texte, pour eviter l'effet "tout serre" quand le theme ne marge pas les
	# paragraphes. On n'ajoute la classe que si l'element n'a pas deja d'attribut
	# class, pour ne pas ecraser un style existant.
	import re
	if not html_text:
		return html_text
	# Plus d'espace entre paragraphes (mb-4) et au-dessus des titres internes
	# (mt-5), texte justifie. L'interligne est gere au niveau du conteneur body.
	rules = (
		('p', 'mb-4 text-justify'),
		('ul', 'mb-4'),
		('ol', 'mb-4'),
		('h3', 'mt-5 mb-3 fw-bold text-o-color-2'),
		('h4', 'mt-5 mb-3 fw-bold text-o-color-2'),
	)
	for tag, classes in rules:
		def add_classes(match):
			attrs = match.group(1) or ''
			class_match = re.search(r'\bclass=(["\'])(.*?)\1', attrs, flags=re.IGNORECASE)
			if class_match:
				existing = class_match.group(2).split()
				merged = existing + [name for name in classes.split() if name not in existing]
				attrs = (
					attrs[:class_match.start()]
					+ 'class=' + class_match.group(1) + ' '.join(merged) + class_match.group(1)
					+ attrs[class_match.end():]
				)
			else:
				attrs += ' class="' + classes + '"'
			return '<' + tag + attrs + '>'

		html_text = re.sub(
			r'<' + tag + r'([^>]*)>',
			add_classes,
			html_text,
			flags=re.IGNORECASE,
		)
	return html_text


def parse_str(str_or_null):
	str_result = ''
	try:
		if isinstance(str_or_null, str):
			if str_or_null:
				str_result = str_or_null
			else:
				str_result = ''
		else:
			str_result = ''
	except Exception as e:
		str_result = ''
	return str_result


def convert_row_to_blog_post(sheet,row, i, record=None):
	blog_post = {}
	blog_post_fr = {}
	if record:
		# Le nom du blog/website est un champ traduit : la recherche depend de la
		# langue du contexte. L'utilisateur qui lance l'import peut etre en fr_FR,
		# alors que le fichier fournit les noms en anglais (les posts sont crees en
		# en_US). On force donc le lookup en en_US pour qu'il soit independant de
		# la langue de l'utilisateur.
		env_en = record.env(context=dict(record.env.context, lang='en_US'))
		blog = env_en['blog.blog'].sudo().search([('name', '=', row[0].value)], limit=1)
		website = env_en['website'].sudo().search([('name', '=', row[5].value)], limit=1)
		author = env_en['res.users'].sudo().search([('email', '=', row[6].value)], limit=1)
		if not blog:
			raise ValueError("Blog introuvable (col 0) : %r" % (row[0].value,))
		if not website:
			raise ValueError("Website introuvable (col 5) : %r" % (row[5].value,))
		if not author:
			raise ValueError("Auteur introuvable (col 6) : %r" % (row[6].value,))
		blog_post['blog_id'] = blog.id
		blog_post['website_id'] = website.id
		blog_post['author_id'] = author.partner_id.id

	# Champs SEO (traduisibles dans Odoo) : version EN sur le post cree en en_US,
	# version FR ecrite ensuite dans le contexte fr_FR (cf. models.py).
	blog_post['website_meta_title'] = row[8].value
	blog_post['website_meta_description'] = row[10].value
	blog_post['website_meta_keywords'] = row[12].value
	blog_post['is_published'] = eval(row[14].value)
	blog_post['active'] = eval(row[15].value)
	blog_post['post_date'] = datetime.datetime.strptime(row[7].value, '%d/%m/%Y %H:%M:%S')

	blog_post['name'] = row[1].value
	blog_post['subtitle'] = row[3].value
	# Versions francaises : lues directement dans les colonnes FR dediees du
	# fichier. Plus d'API de traduction : si la cellule FR est vide, le champ FR
	# reste vide. col 2 = name, 4 = subtitle, 9/11/13 = meta title/desc/keywords.
	blog_post_fr['name'] = parse_str(row[2].value)
	blog_post_fr['subtitle'] = parse_str(row[4].value)
	blog_post_fr['website_meta_title'] = parse_str(row[9].value)
	blog_post_fr['website_meta_description'] = parse_str(row[11].value)
	blog_post_fr['website_meta_keywords'] = parse_str(row[13].value)
	# Titre du post : sert de texte alt par defaut pour les images (SEO/a11y).
	post_title = parse_str(row[1].value)
	why_img = None
	how_img = None
	what_img = None
	conclusion_img = None
	if sheet._images:
		for img in sheet._images:
			# Obtenir les coordonnées de l'ancre de l'image
			anchor = img.anchor
			try:
				row_start, col_start = anchor._from.row, anchor._from.col
				if row_start == i and col_start == 24:
					if record:
						attach_id = add_attachment_file(img, record, i, col_start)
						blog_post['cover_properties'] = '{"background-image": "url(' + attach_id.local_url + ')", "background_color_class": "o_cc3 o_cc", "background_color_style": "", "opacity": "0.2","resize_class": "o_half_screen_height o_record_has_cover", "text_align_class": ""}'
					#img.show()
				if row_start == i and col_start == 25:
					if record:
						attach_id = add_attachment_file(img, record, i, col_start)
						why_img = attach_id
					#img = PILImage.open(img.ref)
					#img.show()
				if row_start == i and col_start == 26:
					if record:
						attach_id = add_attachment_file(img, record, i, col_start)
						how_img = attach_id
					#img = PILImage.open(img.ref)
					#img.show()
				if row_start == i and col_start == 27:
					if record:
						attach_id = add_attachment_file(img, record, i, col_start)
						what_img = attach_id
					#img = PILImage.open(img.ref)
					#img.show()
				if row_start == i and col_start == 28:
					if record:
						attach_id = add_attachment_file(img, record, i, col_start)
						conclusion_img = attach_id
					#img = PILImage.open(img.ref)
					#img.show()
			except Exception as e:
				pass
	# --- New design helpers -------------------------------------------------
	# Each editorial section is rendered as:
	#   1. a coloured "header" block: small red marker (h6.text-primary) above a
	#      large sub-heading (h2), inside a themed text block;
	#   2. the body text coming from the Excel cell (kept as raw builder HTML);
	#   3. the section image full-width underneath (s_picture), when present.
	# Colours follow the website theme via o_cc colour-combination classes, so
	# the article stays re-themable from the builder.

	def _section_header(marker, heading):
		# Pas de fond colore (o_cc*) : titre sur fond clair, comme la maquette.
		# Surtitre rouge + grande question (h2 bleu thème). Largeur de lecture
		# limitee (col-lg-8) pour une meilleure ergonomie typographique.
		return (
			'<section class="s_text_block o_colored_level pt24 pb8" '
			'data-snippet="s_text_block" data-name="Text" style="background-image: none;">\n'
			' <div class="container">\n'
			'  <div class="row"><div class="col-12">\n'
			'   <h5 class="text-primary fw-bold text-uppercase mb-2" style="letter-spacing:.08em;font-size:.9rem;">' + marker + '</h5>\n'
			'   <h2 class="mb-0 text-o-color-2 fw-bold">' + heading + '</h2>\n'
			'  </div></div>\n'
			' </div>\n'
			'</section>\n'
		)

	def _section_body(text):
		# Corps de texte dans une colonne de lecture confortable (col-lg-10).
		# Reglages typographiques au niveau du conteneur (heritage aux <p>) :
		#  - font-size 1.2rem : contenu plus grand ;
		#  - line-height 1.55 : interligne plus serre (moins d'air entre lignes) ;
		#  - text-align justify : texte justifie.
		# Les marges entre blocs (mb-4 / mt-5) viennent de _space_paragraphs.
		body = _space_paragraphs(parse_str(text))
		return (
			'<section class="s_text_block o_colored_level pt8 pb24" '
			'data-snippet="s_text_block" data-name="Text" style="background-image: none;">\n'
			' <div class="container">\n'
			'  <div class="row"><div class="col-12 s_allow_columns">\n'
			'   <div style="font-size:1.2rem;line-height:1.55;text-align:justify;">\n'
			+ body +
			'   </div>\n'
			'  </div></div>\n'
			' </div>\n'
			'</section>\n'
		)

	def _summary(text):
		# Bloc resume / intro mis en avant, rendu en haut de l'article (avant
		# la section "Pourquoi"). Vide si la cellule Resume (col 21) est vide.
		body = parse_str(text)
		if not body:
			return ""
		# Intro mise en avant sans rectangle colore : un liseret rouge a gauche.
		return (
			'<section class="s_text_block o_colored_level pt48 pb24" '
			'data-snippet="s_text_block" data-name="Text" style="background-image: none;">\n'
			' <div class="container">\n'
			'  <div class="row"><div class="col-12">\n'
			'   <div class="ps-4 py-2" style="border-left:4px solid var(--o-color-1, #F00512);">\n'
			'    <div class="mb-0" style="font-size:1.3rem;line-height:1.5;text-align:justify;">' + body + '</div>\n'
			'   </div>\n'
			'  </div></div>\n'
			' </div>\n'
			'</section>\n'
		)

	def _section_picture(img, alt='', compact=False):
		# SEO : un texte alt descriptif est important pour le referencement et
		# l'accessibilite. On l'echappe pour ne pas casser l'attribut HTML.
		if not img:
			return ""
		alt_attr = html.escape(alt or post_title or '', quote=True)
		# Mode compact (images why/how/what) : bandeau de 100px de haut sur toute
		# la largeur, image rognee/centree (object-fit cover + position center)
		# pour remplir la zone sans deformation. On RETIRE 'img-fluid' (qui force
		# height:auto !important et bride la largeur) et on passe les dimensions
		# en !important pour battre les regles residuelles du theme.
		if compact:
			img_classes = 'mx-auto d-block o_we_custom_image'
			image_style = ('height:100px !important;width:100% !important;'
				'object-fit:cover;object-position:center;')
		else:
			img_classes = 'figure-img img-fluid mx-auto d-block o_we_custom_image'
			image_style = ''
		return (
			'<section class="s_picture o_colored_level pt0 pb16" '
			'data-snippet="s_picture" data-name="Image" style="">\n'
			' <div class="container">\n'
			'  <div class="row s_nb_column_fixed">\n'
			'   <div class="col-12 o_colored_level" style="text-align: center;">\n'
			'    <figure class="figure m-0 w-100">\n'
			'     <img src="' + img.local_url + '" class="' + img_classes + '" '
			'alt="' + alt_attr + '" loading="lazy" data-original-src="' + img.local_url + '" data-mimetype="image/png" '
			'style="' + image_style + '">\n'
			'    </figure>\n'
			'   </div>\n'
			'  </div>\n'
			' </div>\n'
			'</section>\n'
		)

	def _advantages(html_block):
		# Section optionnelle : le premier <h3> est le titre, suivi du HTML de
		# l'accordeon. Le HTML (EN ou FR) provient directement de la colonne Excel
		# correspondante. Ainsi aucun texte visible n'est code en dur dans l'importeur.
		raw = parse_str(html_block)
		if not raw.strip():
			return ""
		title, block = _split_heading(raw)
		# Rend les IDs uniques par post : le HTML colle depuis le builder a des
		# IDs figes (myCollapse...). Si plusieurs articles avec accordeon sont
		# sur la meme page (liste de blog), les IDs entrent en collision. On
		# prefixe donc tout ID/ancre 'myCollapse*' par la ligne du post.
		import re as _re
		block = _re.sub(r'myCollapse', 'oaasAdv%d_' % i, block)
		title_html = (
			'   <h3 class="mb-3 fw-bold text-o-color-2">' + title + '</h3>\n'
			if title else ''
		)
		return (
			'<section class="s_faq_collapse o_colored_level pt16 pb8" '
			'data-snippet="s_faq_collapse" data-name="FAQ" style="background-image: none;">\n'
			' <div class="container">\n'
			'  <div class="row"><div class="col-12">\n'
			+ title_html
			+ block + '\n'
			'  </div></div>\n'
			' </div>\n'
			'</section>\n'
		)

	# Accordeon optionnel, pilote par l'Excel (col 31 = HTML EN, col 32 = HTML FR).
	advantages_str = _advantages(row[31].value if len(row) > 31 else None)
	advantages_str_fr = _advantages(row[32].value if len(row) > 32 else None)

	# Pour chaque section : le marqueur rouge est fixe (Pourquoi/Comment/Quoi),
	# le GRAND TITRE BLEU est l'accroche extraite du debut de la cellule Excel
	# (1er <h3>). La valeur de cellule passee (EN ou FR) determine la langue.
	# _build_section() assemble header(marqueur+accroche) + corps.
	def _build_section(marker, cell_value):
		raw = parse_str(cell_value)
		heading, rest = _split_heading(raw)
		# Si pas d'accroche en tete de cellule, on retombe sur le marqueur.
		title = heading or marker
		return _section_header(marker, title) + _section_body(rest)

	# Images : alt descriptif (SEO + accessibilite).
	why_pic = _section_picture(why_img, alt=post_title + ' - contexte du projet', compact=True)
	how_pic = _section_picture(how_img, alt=post_title + ' - demarche projet', compact=True)
	what_pic = _section_picture(what_img, alt=post_title + ' - resultat du projet', compact=True)

	# Conclusion image (full-width, optional) + closing call-to-action banner.
	conclusion_pic = _section_picture(conclusion_img, alt=post_title + ' - synthese')

	def _cta(overline, title, lead, btn_label):
		# CTA final : carte centree, fond du theme (o_cc4 violet), coins
		# arrondis + ombre, surtitre + titre + accroche + bouton avec fleche.
		return (
			'<section class="s_call_to_action o_cc o_cc4 pt64 pb64 o_colored_level" '
			'data-snippet="s_call_to_action" data-name="Appel a l&amp;#x27;action" style="background-image: none;">\n'
			' <div class="container">\n'
			'  <div class="row justify-content-center">\n'
			'   <div class="col-lg-10 text-center o_colored_level rounded-4 shadow-lg px-4 py-5" '
			'style="background-color: var(--o-color-2, #322783);">\n'
			'    <h6 class="text-uppercase fw-bold mb-2" style="letter-spacing:.12em;opacity:.75;">' + overline + '</h6>\n'
			'    <h2 class="fw-bold mb-3 text-white">' + title + '</h2>\n'
			'    <p class="lead mb-4 mx-auto text-white" style="max-width:640px;opacity:.9;">' + lead + '</p>\n'
			'    <a class="btn btn-primary btn-lg px-5 py-3 fw-bold" href="/contactus" '
			'title="' + html.escape(btn_label, quote=True) + '">' + btn_label + ' &#8594;</a>\n'
			'   </div>\n'
			'  </div>\n'
			' </div>\n'
			'</section>\n'
		)

	conclusion_str = conclusion_pic + _cta(
		'Get in touch',
		'Do you want a project like this one?',
		'Tell us about your project - our team will help you turn your needs into a concrete, reliable solution.',
		'Contact us',
	)
	conclusion_str_fr = conclusion_pic + _cta(
		'Parlons-en',
		'Vous voulez un projet comme celui-ci ?',
		'Parlez-nous de votre projet - transformons vos besoins en solution concrète et fiable.',
		'Contactez-nous',
	)

	# Resume / intro : col 29 (EN), col 30 (FR), rendu en tete d'article.
	summary_str = _summary(row[29].value if len(row) > 29 else None)
	summary_str_fr = _summary(row[30].value if len(row) > 30 else None)

	# Assemble: summary (intro), puis chaque section = header(marqueur+accroche)
	# + corps + image. Pour Why, l'image est placee AU-DESSUS de la section
	# (avant le titre rouge) ; l'accordeon "Your benefits" suit la section Why.
	# EN : Why/How/What/Conclusion = col 16/18/20/22. FR : col 17/19/21/23.
	blog_post['content'] = (
		summary_str +
		why_pic + _build_section('Why ?', row[16].value) + advantages_str +
		_build_section('How ?', row[18].value) + how_pic +
		_build_section('What ?', row[20].value) + what_pic +
		_build_section('Conclusion', row[22].value) + conclusion_str
	)

	blog_post_fr['content'] = (
		summary_str_fr +
		why_pic + _build_section('Pourquoi ?', row[17].value) + advantages_str_fr +
		_build_section('Comment ?', row[19].value) + how_pic +
		_build_section('Quoi ?', row[21].value) + what_pic +
		_build_section('Conclusion', row[23].value) + conclusion_str_fr
	)
	return blog_post, blog_post_fr


if __name__ == '__main__':
	connection = None
	try:
		connection = odoo.sql_db.db_connect(to=URI, allow_uri=True)
		# Create a cursor to perform database operations
		cursor = connection.cursor()
		cursor.execute("SELECT version();")
		# Fetch result
		record = cursor.fetchone()
		print("You are connected to - ", record, "\n")
		#TODO : faire la connection avec api.Envrionment pour les tests automatisés
		# loading the Excel File and the sheet
		pxl_doc = openpyxl.load_workbook("D:\\OneDrive - OAAS\\Marketing\\12-SiteWeb\\V4\\OAAS_BLOG_POSTs.xlsx")
		sheet = pxl_doc['Blog import']
		images = sheet._images
		print(f"Nombre d'images trouvées : {len(images)}")

		i = 0
		for row in sheet.iter_rows():
			if i > 0:
				blog, blog_fr = convert_row_to_blog_post(sheet,row, i)
			i = i + 1

	except Exception as e:
		print("Error while connecting to PostgreSQL", str(e))
	finally:
		if (connection):
			cursor.close()
			connection.close()
			print("PostgreSQL connection is closed")




		
		
