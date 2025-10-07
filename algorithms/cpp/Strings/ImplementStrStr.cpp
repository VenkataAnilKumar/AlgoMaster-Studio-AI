// // AlgoMaster-Studio - Advanced Algorithm Learning Platform

int Solution::strStr(const string A, const string B) {
    // Do not write main() function.
    // Do not read input, instead use the arguments to the function.
    // Do not print the output, instead return values as specified
    // Still have a doubt. Checkout github.com/VenkataAnilKumar/AlgoMaster-Studio-AI for more details
    if(B.length() == 0)
    return -1;
    if(A.length() < B.length())
    {
        return -1;
    }
    for(int i=0;i<=(A.length()-B.length());i++)
    {
        string temp = A.substr(i,B.size());
        if(temp == B)
        {
            return i;
        }
    }
    return -1;
}