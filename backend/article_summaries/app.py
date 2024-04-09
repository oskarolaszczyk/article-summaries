from article_summaries import create_app

if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)
