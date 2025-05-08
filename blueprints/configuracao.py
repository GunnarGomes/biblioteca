from flask import Blueprint, render_template, request, session, Response, url_for

style_config = Blueprint('style_config', __name__, template_folder='templates')

@style_config.route('/customize', methods=['GET', 'POST'])
def customize():
    if request.method == 'POST':
       # Salva as preferências do usuário na sessão
       session['bg_color'] = request.form.get('bg_color', '#ffffff')
       session['text_color'] = request.form.get('text_color', '#000000')
    return render_template('configuracao/configuracao.html')

@style_config.route('/dynamic.css')
def dynamic_css():
    # Obtém as preferências da sessão ou usa valores padrão
    bg_color = session.get('bg_color', '#ffffff')
    text_color = session.get('text_color', '#000000')

    # Gera o CSS dinamicamente
    css = f"""
    body {{
       background-color: {bg_color};
       color: {text_color};
       font-family: Arial, sans-serif;
       text-align: center;
       padding: 50px;
    }}
    """
    return Response(css, mimetype='text/css')