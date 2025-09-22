from flask import Flask, render_template, request, jsonify

# Initialize the Flask application
app = Flask(__name__)

# --- Component costs based on the pricing model ---
COST_PER_CPU_CORE = 1.05  # PKR per hour
COST_PER_GB_RAM = 0.70    # PKR per hour
COST_PER_GPU = 128.30     # PKR per hour
MINIMUM_HOURLY_CHARGE = 4.00

def calculate_hpc_price(num_cpu: int, gb_ram: int, num_gpu: int = 0) -> float:
    """Calculates the hourly price for a custom HPC resource slice."""
    cpu_cost = num_cpu * COST_PER_CPU_CORE
    ram_cost = gb_ram * COST_PER_GB_RAM
    gpu_cost = num_gpu * COST_PER_GPU
    total_price = cpu_cost + ram_cost + gpu_cost
    return max(total_price, MINIMUM_HOURLY_CHARGE if num_gpu == 0 else 0)

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """Receives data from the webpage, calculates the price, and returns it."""
    data = request.get_json()
    try:
        cpus = int(data['cpus'])
        ram = int(data['ram'])
        gpus = int(data['gpus'])
        
        # Perform calculation
        price = calculate_hpc_price(num_cpu=cpus, gb_ram=ram, num_gpu=gpus)
        
        # Return the result as JSON
        return jsonify({'price': f'{price:.2f}'})
    except (ValueError, KeyError):
        return jsonify({'error': 'Invalid input. Please provide numbers for all fields.'}), 400

if __name__ == '__main__':
    # Runs the web server
    app.run(debug=True)