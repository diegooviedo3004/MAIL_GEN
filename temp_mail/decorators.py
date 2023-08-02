from functools import wraps
from django.shortcuts import redirect

def sesion_requerida(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'user' not in request.session:  # Reemplaza 'valor_sesion' con el nombre de la clave que deseas verificar
            return redirect('index')  # Reemplaza 'index' con el nombre de la vista a la que deseas redirigir

        return view_func(request, *args, **kwargs)

    return _wrapped_view
