from django.shortcuts import render, redirect
from django.contrib import messages
from . import appsheet

def home(request):
    # renderiza dashboard
    cursos = appsheet.get_all("Cursos")
    cats = appsheet.get_all("Catedraticos")
    return render(request, 'portal/home.html', {'cursos_qty': len(cursos), 'cats_qty': len(cats)})

# cruds de cursos
def curso_list(request):
    cursos = appsheet.get_all("Cursos")
    catedraticos = appsheet.get_all("Catedraticos")
    
    # Mapear el Row_ID al Nombre para visualizacion
    cat_map = {c.get("Row_ID"): c.get("Nombre") for c in catedraticos}
    for curso in cursos:
        curso["Catedratico_Nombre"] = cat_map.get(curso.get("ID_CATEDRATICO"), "No asignado")
        
    return render(request, 'portal/curso_list.html', {'cursos': cursos})

def curso_form(request, id=None):
    # gestiona creacion y edicion de cursos
    curso = appsheet.get_by_id("Cursos", "Row_ID", id) if id else None
    catedraticos = appsheet.get_all("Catedraticos")
    
    if request.method == 'POST':
        data = {
            "Nombre": request.POST.get('nombre'),
            "Categoría": request.POST.get('categoria'),
            "Descripcion": request.POST.get('descripcion'),
            "ID_CATEDRATICO": request.POST.get('id_catedratico')
        }
        if id:
            data["Row ID"] = id # la llave en APPSHEET
            success, msg = appsheet.update_record("Cursos", data)
        else:
            success, msg = appsheet.create_record("Cursos", data)
            
        if success:
            return redirect('curso_list')
        
        # extraemos el mensaje real de AppSheet
        error_detail = msg if isinstance(msg, str) else msg.get('detail', "Error desconocido")
        messages.error(request, f"Error de AppSheet: {error_detail}")
        
    return render(request, 'portal/curso_form.html', {'curso': curso, 'catedraticos': catedraticos})

def curso_delete(request, id):
    appsheet.delete_record("Cursos", id)
    return redirect('curso_list')

# cruds de catedraticos
def catedratico_list(request):
    catedraticos = appsheet.get_all("Catedraticos")
    return render(request, 'portal/catedratico_list.html', {'catedraticos': catedraticos})

def catedratico_form(request, id=None):
    # gestiona creacion y edicion catedraticos
    catedratico = appsheet.get_by_id("Catedraticos", "Row_ID", id) if id else None
    
    if request.method == 'POST':
        data = {
            "Nombre": request.POST.get('nombre'),
            "Especialidad": request.POST.get('especialidad'),
            "email": request.POST.get('email')
        }
        if id:
            data["Row ID"] = id # llave de AppSheet
            success, msg = appsheet.update_record("Catedraticos", data)
        else:
            success, msg = appsheet.create_record("Catedraticos", data)
            
        if success:
            return redirect('catedratico_list')
        
        error_detail = msg if isinstance(msg, str) else msg.get('detail', "Error desconocido")
        messages.error(request, f"Error de AppSheet: {error_detail}")
        
    return render(request, 'portal/catedratico_form.html', {'catedratico': catedratico})

def catedratico_delete(request, id):
    appsheet.delete_record("Catedraticos", id)
    return redirect('catedratico_list')
