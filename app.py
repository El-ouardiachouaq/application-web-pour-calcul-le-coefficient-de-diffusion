#EL-OUARDI ACHOUAQ
from flask import Flask, request, redirect, url_for
import numpy as np

app = Flask(__name__)

# Function to compute the diffusion coefficient and error
def compute_diffusion_coefficient(x_A, D_AB0, D_BA0, q_A, T, D_exp, q_B, a_BA, a_AB, ra, rb):
    # Solvent fraction
    x_B = 1 - x_A
    
    # Tau values
    tau_AB = np.exp(-a_AB / T)
    tau_BA = np.exp(-a_BA / T)
    tau_AA = 1
    tau_BB = 1
    
    # Lambda values
    lambda_A = ra ** (1 / 3)
    lambda_B = rb ** (1 / 3)
    
    # Phi values
    phi_A = x_A * lambda_A / (x_A * lambda_A + x_B * lambda_B)
    phi_B = x_B * lambda_B / (x_A * lambda_A + x_B * lambda_B)
    
    # Theta values
    theta_A = (x_A * q_A) / (x_A * q_A + x_B * q_B)
    theta_B = (x_B * q_B) / (x_A * q_A + x_B * q_B)
    theta_BA = (theta_B * tau_BA) / (theta_A * tau_AA + theta_B * tau_BA)
    theta_AB = (theta_A * tau_AB) / (theta_A * tau_AB + theta_B * tau_BB)
    theta_AA = (theta_A * tau_AA) / (theta_A * tau_AA + theta_B * tau_BA)
    theta_BB = (theta_B * tau_BB) / (theta_A * tau_AB + theta_B * tau_BB)
    
    # HSU-CHEN equation
    term1 = x_B * np.log(D_AB0) + x_A * np.log(D_BA0) + 2 * (x_A * np.log(x_A / phi_A) + x_B * np.log(x_B / phi_B)) + 2 * x_A * x_B * ((phi_A / x_A) * (1 - (lambda_A / lambda_B)) + (phi_B / x_B) * (1 - (lambda_B / lambda_A)))
    term2 = (x_B * q_A) * ((1 - theta_BA ** 2) * np.log(tau_BA) + (1 - theta_BB ** 2) * tau_AB * np.log(tau_AB)) + (x_A * q_B) * ((1 - theta_AB ** 2) * np.log(tau_AB) + (1 - theta_AA ** 2) * tau_BA * np.log(tau_BA))
    
    ln_D_AB = term1 + term2
    D_AB = np.exp(ln_D_AB)
    
    # Error calculation
    error = (np.abs(D_AB - D_exp) / D_exp) * 100
    
    return D_AB, error

# Homepage
@app.route('/')
def home():
    return """
        <html>
            <body>
                <h1>HELLO PIC 12, BEST GROUP 2</h1>
                <p>Welcome to the <u>Diffusion Coefficient Calculator</u>.</p>
                <p>This application allows you to calculate the diffusion coefficient and the relative error compared to an experimental value.</p>
                <p>Click the <b>Next</b> button to begin.</p>
                <a href='/page2'><button>Next</button></a>
            </body>
        </html>
    """

# Input page
@app.route('/page2', methods=['GET'])
def page2():
    return """
        <html>
            <body>
                <h1>Enter the Required Values</h1>
                <p>Please enter the following values to calculate the diffusion coefficient:</p>
                <form action='/page3' method='post'>
                    Molar fraction of A (x_A): <input type='text' name='x_A' value='0.25' required><br><br>
                    Initial diffusion coefficient D_AB0: <input type='text' name='D_AB0' value='2.1e-5' required><br><br>
                    Initial diffusion coefficient D_BA0: <input type='text' name='D_BA0' value='2.67e-5' required><br><br>
                    Radius of A (rA): <input type='text' name='rA' value='1.4311' required><br><br>
                    Radius of B (rB): <input type='text' name='rB' value='0.92' required><br><br>
                    Experimental value of D_AB (DAB_exp): <input type='text' name='DAB_exp' value='1.33e-5' required><br><br>
                    Temperature (T): <input type='text' name='T' value='313' required><br><br>
                    Parameter a_AB: <input type='text' name='a_AB' value='-10.7575' required><br><br>
                    Parameter a_BA: <input type='text' name='a_BA' value='194.5302' required><br><br>
                    Parameter q_A: <input type='text' name='q_A' value='1.432' required><br><br>
                    Parameter q_B: <input type='text' name='q_B' value='1.4' required><br><br>
                    <button type='submit'>Calculate</button>
                </form>
            </body>
        </html>
    """

# Results page
@app.route('/page3', methods=['POST'])
def page3():
    try:
        # Retrieve form values
        x_A = float(request.form['x_A'].replace(',', '.'))
        D_AB0 = float(request.form['D_AB0'])
        D_BA0 = float(request.form['D_BA0'])
        rA = float(request.form['rA'])
        rB = float(request.form['rB'])
        D_AB_exp = float(request.form['DAB_exp'])
        a_AB = float(request.form['a_AB'])
        a_BA = float(request.form['a_BA'])
        T = float(request.form['T'])
        q_A = float(request.form['q_A'])
        q_B = float(request.form['q_B'])

        # Compute diffusion coefficient and error
        D_AB, error = compute_diffusion_coefficient(x_A, D_AB0, D_BA0, q_A, T, D_AB_exp, q_B, a_BA, a_AB, rA, rB)
        
        # Display results
        return f"""
            <html>
                <body>
                    <h1><i>Final Result</i></h1>
                    <p>The diffusion coefficient D_AB is: <b>{D_AB:.3e} cm²/s</b></p>
                    <p>The relative error compared to the experimental value is: <b>{error:.2f} %</b></p>
                    <p>Thank you for using our calculator!</p>
                    <a href="/">Return to Homepage</a>
                </body>
            </html>
        """
    except ValueError:
        return """
            <html>
                <body>
                    <h1>Error: Invalid Input</h1>
                    <p>Please enter valid numerical values.</p>
                    <a href="/page2">Back to Form</a>
                </body>
            </html>
        """

# Error handling for non-existent routes
@app.errorhandler(404)
def page_not_found(e):
    return """
        <html>
            <body>
                <h1>HELLO PIC 12, BEST GROUP 2</h1>
                <p>Welcome to the Diffusion Coefficient Calculator.</p>
                <p style='color: red;'>The requested page does not exist. You have been redirected to the homepage.</p>
                <a href='/page2'><button>Next</button></a>
            </body>
        </html>
    """, 404

if __name__ == '__main__':
    app.run(debug=True)
    
