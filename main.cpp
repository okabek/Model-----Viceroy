#include <iostream>
#include <vector>
#include <cmath>

using namespace std; 

//

vector<double> matrix_multiply(vector<double> x, vector<double> y)
{
    vector<double> xy;
    
    for (int i = 0; i < x.size(); i++)
    {
        for (int i2 = 0; i2 < y.size(); i2++)
        {
            xy.push_back(i * i2);
        }
    }
    
    
    return (xy);
}


class crysalis
{
    public:
        int hidden_size = 4;
        int hidden_layers = 1;
        int output_size = 1;
        double learning_rate = 0.01;
        double last_mse = 999;
    
        vector<double> inputs;
        vector<vector<double>> weights;
        vector<vector<double>> biases;
        vector<vector<double>> hidden;
        vector<double> outputs;
        
        void init()
        {
            weights.resize(hidden_layers + 1);
            weights[0].resize(inputs.size() * hidden_size);
            weights[hidden_layers].resize(hidden_size * output_size);
            hidden.resize(hidden_layers);
            outputs.resize(output_size);

            if (hidden_layers >= 2)
            {
                for (int i = 1; i < hidden_layers - 1; i++)
                {
                    weights[i].resize(hidden_size * hidden_size);
                }
            }
            
            
            for (int i = 0; i < weights.size(); i++)
            {
                for (int i2 = 0; i2 < weights[i].size(); i2++)
                {
                    weights[i][i2] = rand() % 10 / 10.0;
                }
            }
            
            
            for (int i = 0; i < hidden.size(); i++)
            {
                hidden[i].resize(hidden_size);
            }
            
            
            biases = hidden;
        }
        
        
        double activate(double x)
        {
            return(tanh(x));
        }
        
        
        double activate_derivative(double x)
        {
            return(1 - x * x);
        }
        
    
        void clear()
        {
            for (int i = 0; i < hidden.size(); i++)
            {
                for (int i2 = 0; i2 < hidden[i].size(); i2++)
                {
                    hidden[i][i2] = 0.0;
                }
            }
        }
    
    
        void feed()
        {
            clear();
            
            for (int i = 0; i < inputs.size(); i++)
            {
                for (int i2 = 0; i2 < hidden[0].size(); i2++)
                {
                    hidden[0][i2] += inputs[i] * weights[0][i * i2] + biases[0][i2];
                }
            }
            
            
            if (hidden_layers > 1)
            {
                
            }
            else 
            {
                for (int i = 0; i < hidden[hidden_layers - 1].size(); i++)
                {
                    for (int i2 = 0; i2 < output_size; i2++)
                    {
                        outputs[i2] = activate(hidden[hidden_layers - 1][i]) * weights[weights.size() - 1][i * i2] + biases[hidden_layers - 1][i];
                    }
                }
            }
        }
        
        
        void get_output()
        {
            for (int i = 0; i < outputs.size(); i++)
            {
                cout << i << " = " << outputs[i] << "\n";
            }
        }
        
        
        void back_prop(double answer)
        {
            double error = outputs[0] - answer;
            double mse = error * error;
            
            // last layer weights
            double cost_derivative = 2 * (outputs[0] - answer);
            
            vector<double> last_hidden_layer = hidden[hidden.size() - 1];
            vector<double> last_weights_layer = weights[weights.size() - 1];
            
            for (int i = 0; i < last_weights_layer.size(); i++)
            {
                double previous_hidden = last_hidden_layer[i];
                
                last_weights_layer[i] -= learning_rate * cost_derivative * activate_derivative(activate(previous_hidden)) * previous_hidden;
            }
            
            
            for (int i2 = 0; i2 < biases[hidden_layers - 1].size(); i2++)
            {
                //biases[hidden_layers - 1][i2] -= learning_rate * cost_derivative;
            }
            
            
            // first layer weights
            for (int i = 0; i < inputs.size(); i++)
            {
                for (int i2 = 0; i2 < weights[0].size(); i2++)
                {
                    //weights[0][i2] += learning_rate * activate_derivative(hidden[0][i2]);
                }
            }
            
            
            mse /= outputs.size();
            last_mse = mse;
            
            cout << "MSE = " << mse << "\n";
        }
};

//

int main() {
    crysalis nn; 
    nn.inputs = {3, 2};
    nn.init();
    
    for (int i = 0; i < 1000; i++)
    {
        double answer = i * 2;
        
        nn.inputs = {(double)i, 2};
        nn.feed();
        nn.back_prop(answer);
        
        if (nn.last_mse <= 0.001) 
        {
            cout << "STOPPING EARLY!" << endl;
            
            break;
        }
    }
    

    nn.inputs = {10, 2};
    nn.feed();
    nn.get_output();
        
    return 0;
}
