from flask import Flask, request, render_template
import numpy as np

app = Flask(__name__)

def get_model_size_in_bytes(size_option, size_value):
    if size_option == 'bytes':
        return int(size_value), size_value
    elif size_option == 'tensors':
        dimensions = [int(dim) for dim in size_value.split(',')]
        size_in_bytes = np.prod(dimensions, dtype=np.int64) * 4  # Use np.int64 to avoid overflow
        return size_in_bytes, ', '.join(map(str, dimensions))
    else:
        raise ValueError('Invalid size option')




@app.route('/', methods=['GET', 'POST'])
def estimate_bandwidth():
    if request.method == 'POST':
        N = int(request.form['N'])
        size_option = request.form['size_option']
        size_value = request.form['size_value']
        P, P_value = get_model_size_in_bytes(size_option, size_value)
        U = int(request.form['U'])
        
        bandwidth = N * P * U  # Bandwidth estimation formula

        # Convert bandwidth to Megabytes for user-friendly display
        bandwidth_in_mb = bandwidth / (1024 * 1024)
        
        return render_template('result.html', bandwidth=bandwidth_in_mb, N=N, P=P, U=U, P_value=P_value, size_option=size_option)
    else:
        return render_template('form.html')
if __name__ == "__main__":
    app.run(debug=True)
