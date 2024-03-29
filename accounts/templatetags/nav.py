from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def custom_li(request, link_name, link, current_url_name, content, css_classes="" ):
    print_active = ""
    if current_url_name ==link_name : #EX: request.resolver_match.url_name == profile
        print_active = "active"
        
    link = request.build_absolute_uri(reverse(link)) #EX "accounts:profile" => https://domain.com/profile
    # link = reverse(link)                           #EX "accounts:profile" => /profile
    html = '''<li class="nav-item">''' + \
        f'<a href="{link}" class="nav-link {print_active}"> ' +\
        f'<i class="far {css_classes} nav-icon "></i>' +\
        f'<p>{content}</p>' +\
        '''</a>''' +\
        '''</li>'''
    return html

#{% autoescape off %} #convert str to html
# {% custom_li  request "profile" "accounts:profile" request.resolver_match.url_name  "پروفایل" "fa-user" %}
#{% endautoescape %}