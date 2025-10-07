// // AlgoMaster-Studio - Advanced Algorithm Learning Platform

int Solution::maxArea(vector<int> &A) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout github.com/VenkataAnilKumar/AlgoMaster-Studio-AI for more details
            
    int i = 0;
    int j = A.size()-1;
    int ans = 0;
    
    while(i < A.size()){
        int curr = 0;
        if(A[i] <= A[j]){
            curr = (j-i)*A[i];
            i++;
        }
        else{
            curr = (j-i)*A[j];
            j--;
        }
        if(curr > ans){
            ans = curr;
        }
        if(i == j){
            break;
        }
    }
    
    return ans;
    
}
