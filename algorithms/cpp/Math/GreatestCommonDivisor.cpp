// // AlgoMaster-Studio - Advanced Algorithm Learning Platform

int Solution::gcd(int A, int B) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout github.com/VenkataAnilKumar/AlgoMaster-Studio-AI for more details

    while(A != 0){
        int temp = B;
        B = A;
        A = temp%A;
    }
    
    return B;
}
