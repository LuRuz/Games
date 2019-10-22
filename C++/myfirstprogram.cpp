#include <iostream>
#include <string>

using namespace std;

int main(){
    string test;
    cout << "Introduzca string: "; //Output text
    //cin >> x; //Get user input from keyboard. ONLY FOR SIMPLE WORDS
    getline (cin, test); //Imput line from keyboard
    cout << "El string introducido: " << test;

    cout << "\n";
    int y=1;
    y <<= 2;    //Mueve el bit 1, dos elementos hacia la izda
    cout << y;
    cout << "\n";

    string z= "prueba \n";
    cout << z.length(); //La longitud del string incluye solo los caracteres


    return 0;
}
