// // AlgoMaster-Studio - Advanced Algorithm Learning Platform

int Solution::isValid(string A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout github.com/VenkataAnilKumar/AlgoMaster-Studio for more details
    
    stack<char> mySt;
    
    for(int i = 0; i < A.size(); i++){
        if(A[i] == '['){
            mySt.push(A[i]);
        }
        else if(A[i] == '('){
            mySt.push(A[i]);
        }
        else if(A[i] == '{'){
            mySt.push(A[i]);
        }
        else if(A[i] == ']'){
            if(!mySt.empty()){
                if(mySt.top() == '['){
                    mySt.pop();
                }
                else{
                    return 0;
                }
            }
            else{
                return 0;
            }
        }
        else if(A[i] == ')'){
            if(!mySt.empty()){
                if(mySt.top() == '('){
                    mySt.pop();
                }
                else{
                    return 0;
                }
            }
            else{
                return 0;
            }
        }
        else if(A[i] == '}'){
            if(!mySt.empty()){
                if(mySt.top() == '{'){
                    mySt.pop();
                }
                else{
                    return 0;
                }
            }
            else{
                return 0;
            }
        }
        
    }
    
    if(mySt.empty()){
        return 1;
    }
    
    return 0;
}
