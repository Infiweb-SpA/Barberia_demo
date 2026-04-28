import os
from app import create_app

# Creamos la instancia de la aplicación usando tu fábrica de apps
app = create_app()

if __name__ == '__main__':
    # Railway requiere que la app escuche en el host 0.0.0.0
    # y en el puerto definido por la variable de entorno PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)