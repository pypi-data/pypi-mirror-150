from models.definition import Action
from models.element import LoginElement,SecurityElement,ButtonElement

url="https://tfwp-jb.lmia.esdc.gc.ca/employer/",

login_para = {
        "action_type":Action.Login.value,
        "rcic":"jacky",
        "portal":"lmiaportal",
        "account_element_id": "#loginForm\\:input-email",
        "password_element_id": "#loginForm\\:input-password",
        "login_button_id":
            "#loginForm\\:j_id_3z > span",
        "success_element_id":
            "#wb-cont"
    }

security_element = {
    "action_type":Action.Security.value,
    "portal":"lmiaportal",
    "question_element_id":"#securityForm > fieldset > div > p",
    "answer_element_id": "#securityForm\\:input-security-answer",
    "continue_element_id": "#continueButton",
    "success_element_id":"#modal-accept",
    "security_answers":{
        "significant other":"Shanghai",
        "childhood best":"dongfang",
        "first trip":"China"
    }
}

button={
    "action_type":Action.Button.value,
    "label":"Agree",
    "id":"#modal-accept"
}
# get a RCIC name and return login scripts for javascript filling
def login(rcic):
    login_para['rcic']=rcic
    login=LoginElement(**login_para)
    
    security_element['rcic']=rcic
    se=SecurityElement(**security_element)

    # click Agree button 
    btn=ButtonElement(**button)
    return [login.make(),se.make(),btn.make()]