// // AlgoMaster-Studio - Advanced Algorithm Learning Platform

string Solution::reverseString(string A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout github.com/VenkataAnilKumar/AlgoMaster-Studio-AI for more details
    stack<char> rev;
    
    for(int i = 0; i < A.size(); i++){
        rev.push(A[i]);
    }
    
    string ans = "";
    
    int height = rev.size();
    
    
    for(int i = height-1; i >= 0; i--){
        ans = ans + rev.top();
        rev.pop();
    }
    
    return ans;
}
