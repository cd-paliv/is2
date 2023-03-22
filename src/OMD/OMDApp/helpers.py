from OMD.settings import DEFAULT_FROM_EMAIL, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from django.core.mail import get_connection, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def email_sender(html_template, html_context: dict, subject, email, file_attachment=None) -> int:
    html_message = render_to_string(html_template, html_context)
    html_text=strip_tags(html_message)
    connection = get_connection(username=EMAIL_HOST_USER, password=EMAIL_HOST_PASSWORD)

    mail = EmailMultiAlternatives(
    subject, html_text, from_email=DEFAULT_FROM_EMAIL, to=[email], connection=connection
    )
    mail.attach_alternative(html_message, "text/html")

    if file_attachment:
        mail.attach("comprobante.pdf", content=file_attachment, mimetype="application/pdf")
    return mail.send()