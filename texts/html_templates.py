PAGE_TEMPLATE = """
<p><b><a href="{invite_project_url}">Предложить автору проект 🤝</a></b></p>
<p><b>Количество сделок 📝:</b> {deals_amount}</p>
<p><b>Предметы 📚:</b> {subjects}</p>

<p><b>Биография 👤:</b></p>
<blockquote>{biography}</blockquote>

<h3>Средний рейтинг 🌟:</h3>
{avg_rating}

<h3>Примеры работ 🎓:</h3>
<p>{images}</p>

<h3>Отзывы ({reviews_amount}):</h3>
{reviews}
"""

REVIEW_TEMPLATE = """
<aside>{client_name}:</aside>
<blockquote>{text}</blockquote>
<p>Качество: {quality}</p>
<p>Сроки: {terms}</p>
<p>Контактность: {contact}</p>\
"""

AVG_RATING_TEMPLATE = """
<p>Качество: {quality} ({quality_num:.2f})</p>
<p>Сроки: {terms} ({terms_num:.2f})</p>
<p>Контактность: {contact} ({contact_num:.2f})</p>
"""
