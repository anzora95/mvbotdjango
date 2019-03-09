import smtplib

#parametros:
#Correo Destinatario //addressee
#contraseña destinatario  //adds_pass
#Correo receptor  //receiver
#Cuerpo del mensaje dependiendo del tipo de notificacion //body_m

def mail_notify(body_m,addressee,receiver,adds_pass):
    content= body_m
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    mail.login(addressee, adds_pass)
    mail.sendmail(addressee,receiver,content)
    mail.close()