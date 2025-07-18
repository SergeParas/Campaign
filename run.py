from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


    # * un accès admin sur `/admin/login` (identifiant : admin, mot de passe : admin)
    #* les invités peuvent répondre sur `/guest/`
