// // AlgoMaster-Studio - Advanced Algorithm Learning Platform

void Solution::arrange(vector<int> &A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout github.com/VenkataAnilKumar/AlgoMaster-Studio-AI for more details
    
    for(int i = 0; i < A.size(); i++){
        A[i] = A[i] + (A[A[i]]%(A.size()))*A.size();
    }
    
    for(int i = 0; i < A.size(); i++){
        A[i] = A[i]/A.size();
    }
}
