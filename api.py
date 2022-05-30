from flask import Flask, request, render_template
import rec_main

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/tables", methods=["GET"])
def result_tables():

    if "id" in request.args:
        productid_list = request.args["id"][1:-1].replace('"', "").split(sep=",")
    else:
        productid_list = None

    data = rec_main.hayde(product_ids=productid_list)
    return render_template(
        "view.html",
        tables=[
            data[1].to_html(classes="male"),
            data[0].to_html(classes="female"),
        ],
        titles=["na", "Cart Page", "Related Products"],
    )


app.run()