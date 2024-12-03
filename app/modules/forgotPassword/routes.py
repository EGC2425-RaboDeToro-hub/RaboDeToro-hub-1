from flask import flash, redirect, render_template, request, url_for
from app.modules.auth.decorators import guest_required
from app.modules.forgotPassword import forgotPassword_bp
from app.modules.forgotPassword.services import ForgotpasswordService

forgotPasswordService = ForgotpasswordService()


@forgotPassword_bp.route('/forgotPassword/forgot', methods=['GET', 'POST'])
@guest_required
def forgot():
    if request.method == "POST":

        try:
            email = request.form["email"]
            print(email)
            token = forgotPasswordService.sendEmail(email=email)
            print(token)
            forgotPasswordService.addToken(token=token)
            print("Token added")
            flash(
                "Email sent. Check your inbox and follow the instrucctions.",
                "success",
            )
        except Exception as exc:
            flash(
                f"ERROR: {exc}", "danger"
            )

        return redirect(url_for("auth.login"))
    return render_template("resetPassword/forgotPasswordRequest.html")


@forgotPassword_bp.route("/forgotPassword/password/<token>", methods=["GET", "POST"])
@guest_required
def resetPassword(token):

    forgotPasswordService.checkToken(token)
    email = forgotPasswordService.getEmailToken(token)

    if forgotPasswordService.checkUsedToken(token):
        flash("Repeated link.", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        password = request.form["password"]
        forgotPasswordService.resetPassword(email=email, password=password)
        forgotPasswordService.usedToken(token)
        flash("Password successfully changed!", "success")
        return redirect(url_for("auth.login"))
    return render_template("resetPassword/forgotPasswordConfirmation.html")
