// csvAutomate.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <fstream>

using namespace std;
int main()
{
    ofstream output;
    output.open("yayeet500.csv");
    if (!output) return 1;
    for (int i = 500; i <= 511; i++) output << ",gs://bucketoforders/boba_training_data/file" << i << ".jsonl" << endl;
    output.close();
    cout << "Hello World!\n";
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu