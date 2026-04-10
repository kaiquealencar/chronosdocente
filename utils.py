from sqlalchemy import select, desc
from extensions import db

def is_admin(current_user):
    return current_user.is_authenticated and getattr(current_user, 'is_admin', False)

def criar_paginacao(request, model_class, current_user, ordenar_por=None, descendente=False):
    try:
         page = request.args.get('page', 1, type=int)

         if page < 1:
              page = 1
    except (TypeError, ValueError):
         page =1 
    
    query = select(model_class)
    user_admin = is_admin(current_user)

    if not user_admin:
         query = query.where(model_class.usuario_id == current_user.id)
    
    if ordenar_por:
         coluna = getattr(model_class, ordenar_por, None)

         if coluna is not None:
               
               if descendente:
                    query = query.order_by(desc(coluna))
               else:                 
                    query = query.order_by(coluna)

    pagination = db.paginate(query, page=page, per_page=6, error_out=False)

    return [pagination, user_admin]
            
  


