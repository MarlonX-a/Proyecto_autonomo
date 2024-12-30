from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

#funcion que valida el número de cedula
def validar_cedula(value):
    """Valida que el número de cédula ecuatoriana sea correcto."""
    if not value.isdigit() or len(value) != 10:
        raise ValidationError("La cédula debe tener exactamente 10 dígitos numéricos.")
    
    digitos = [int(d) for d in value]
    provincia = int(value[:2])
    if not (1 <= provincia <= 24 or provincia == 30):
        raise ValidationError("El código de provincia no es válido.")
    
    if digitos[2] > 6:
        raise ValidationError("El tercer dígito no es válido para una cédula ecuatoriana.")
    
    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    suma = 0
    for i in range(9):
        producto = digitos[i] * coeficientes[i]
        if producto >= 10:
            producto -= 9
        suma += producto
    
    digito_verificador = 10 - (suma % 10) if suma % 10 != 0 else 0
    if digito_verificador != digitos[9]:
        raise ValidationError("La cédula es inválida.")
    

#funcion que valida el número de celular
def validar_numero_celular(value):
    """Valida que el número de celular ecuatoriano sea válido."""
    if not value.isdigit():
        raise ValidationError("El número de celular solo debe contener dígitos.")
    
    if len(value) != 10:
        raise ValidationError("El número de celular debe tener exactamente 10 dígitos.")
    
    if not value.startswith('09'):
        raise ValidationError("El número de celular debe comenzar con '09'.")



class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _("Tu contraseña debe tener al menos 8 caracteres."),
                code='password_too_short',
            )
        if password.isdigit():
            raise ValidationError(
                _("Tu contraseña no puede ser completamente numérica."),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _("Tu contraseña debe tener al menos 8 caracteres y no puede ser completamente numérica.")