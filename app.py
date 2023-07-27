from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def estimate_bandwidth():
    N = request.form.get('N')
    U = request.form.get('U')
    size_option = request.form.get('size_option')
    size_value = request.form.get('size_value')

    # Ensure the values are integers
    try:
        N = int(N)
        U = int(U)
    except ValueError:
        return "Error: N and U inputs must be numbers."

    # If size option is tensors, calculate size in bytes assuming float32 (4 bytes) per parameter
    if size_option == 'tensors':
        try:
            dims = [int(dim) for dim in size_value.split(',')]
            size_value = 4 * prod(dims)  # Assuming float32 (4 bytes) per parameter
        except:
            return "Error: Tensor dimensions must be comma-separated integers."
    else:  # size option is 'manual'
        try:
            size_value = float(size_value)
        except ValueError:
            return "Error: Manual size must be a number."

    # Calculate bandwidth
    bandwidth_bytes =  N * size_value * U
    bandwidth_MB = bandwidth_bytes / (1024 * 1024)

    return render_template('result.html', bandwidth=bandwidth_MB)

def prod(lst):
    product = 1
    for number in lst:
        product *= number
    return product

if __name__ == '__main__':
    app.run(debug=True)
