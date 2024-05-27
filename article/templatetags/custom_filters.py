from django import template

register = template.Library()

@register.filter
def divide(value, arg):
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return None
    
@register.simple_tag
def modulo(value, arg):
    try:
        return int(value) % int(arg)
    except (ValueError, ZeroDivisionError):
        return None
    
    
@register.simple_tag
def join_two_lists(list1, list2):
    _list = []
    for i in list1:
        _list.append(i)
    for i in list2:
        _list.append(i)
    return _list

@register.simple_tag
def checked(user_choices, question_id,  input_option):
    ''' if user option is equal to input option Return "checked" '''

    if  len(user_choices) > 0 and user_choices[str(question_id)]["user"] == input_option:
        return 'checked'
    # return None


@register.simple_tag
def is_answer(quiz_is_done, user_option, question_id, input_option):
    ''' if user option is correct Return "text-success" '''
    if quiz_is_done : 
        if user_option[str(question_id)]["answer"] == input_option :
            return 'text-success'
        elif user_option[str(question_id)]["user"] == input_option :
            return 'text-danger'
    return ''

@register.simple_tag
def radio_input_color(quiz_is_done, user_option, question_id, input_option):
    '''  change the radio color input  to either green or red " '''
    if quiz_is_done : 
        if user_option[str(question_id)]["answer"] == input_option :
            return 'correct-form-check-input'
        elif user_option[str(question_id)]["user"] == input_option :
            return 'incorrect-form-check-input'
    return ''






    
