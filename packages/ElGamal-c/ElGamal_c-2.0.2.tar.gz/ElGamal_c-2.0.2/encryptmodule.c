#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include "string.h"
#include "Python.h"

int cis_prime(long long n)
{
    
    long long last = (long long) sqrtl(n) + 1; 

    for (long long j = 2; j <= last; ++j)
    if (n % j == 0)
    

        return 0;
        

    return 1;
}

long long cpow_mod(long long x, long long y, long long z)
{
    long long number = 1;
    while (y)
    {
        if (y & 1)  /* is_even */
            number = number * x % z;
        y >>= 1;  /* diviide 2 */
        x = (unsigned long long)x * x % z;  
    }
    return number;
}

// Mosaed function after optimization
long long cpow_mod3(long long g, long long exp, long long n)
{
    
    if (exp == 0)
        return 1;
    if (exp == 1)
        return g % n;
    if (exp == 2)
        return (g * g) % n;

    long long g_half_exp = cpow_mod3(g, exp>>1, n); // optimization

    return (cpow_mod3(g, exp%2, n) * (g_half_exp*g_half_exp) % n) % n;
}

// Mosaed function after optimization
long long cpow_mod4(long long g, long long exp, long long n)
{
    
    if (exp == 0)
        return 1;
    if (exp == 1)
        return g % n;
    if (exp == 2){
        long long rhs = n-g;
        if (rhs < g)
            g = rhs;

        return (g * g) % n;

    }
    
    long long g_half_exp = cpow_mod4(g, exp>>1, n); // optimization

    return (cpow_mod4(g, exp%2, n) * (g_half_exp*g_half_exp) % n) % n;
}

int cis_primitive_root(int g, int n)
{
    int i;

    for (i = 1; i < n - 1; i++)
    {
        if (cpow_mod4(g, i, n) == 1)
            return 0;
    }

    return 1;
}

int gcd(int a, int b)
{
    // Find Minimum of a and b
    int result = ((a < b) ? a : b);
    while (result > 0) {
        if (a % result == 0 && b % result == 0) {
            break;
        }
        result--;
    }
 
    // Return gcd of a and b
    return result;
}

int cget_second_primitive_root(int p){

    int i, count =0;
    for(i=1; i<p; i++){
        if (cis_primitive_root(i, p)){
            // printf("%d\n", i);
            count++;
            if (count==2) return i;
        }
    }
    return 2;
} 

long long cget_first_primitive_root_loop(long long p){

    long long o = 1;
    long long k;
    for (long long r = 2; r < p; r++) {
        k = cpow_mod(r, o, p);

        while (k > 1) {
            o++;
            k *= r;
            k %= p;
        }
        if (o == (p - 1)) {
            return r;
        }
        o = 1;
    }
    return -1;
} 

long long generator (long long p) {

    
    long* fact = (long*) malloc(p*sizeof(long)); 
    long long index = 0;
    long long phi = p-1,  n = phi;
    for (long long i=2; i*i<=n; ++i)
        if (n % i == 0) {
            fact[index++] = i;
            while (n % i == 0)
                n /= i;
        }
    if (n > 1)
        fact[index++] = n;

    for (long long res=2; res<p; ++res) {
        int ok = 1;
        for (size_t i=0; i<index && ok; ++i)
            ok &= cpow_mod (res, phi / fact[i], p) != 1;
        if (ok) return res;
            
    }
    return -1;
}


unsigned long long long_pow(long long base, long long exp){
    unsigned long long number =1;

    for (int i = 0; i<exp; i++)
        number *= base;

    return number;
}

int generate_c1(int g, int secret, int p){
    return cpow_mod(g, secret, p);
}

void gen_g(int*g, int p){
    *g = cget_second_primitive_root(p);
}
void gen_g_FAST(int *g, int p){
    *g = cget_first_primitive_root_loop(p);
}
void gen_g_FASTEST(long long *g, long long p){
    *g = generator(p);
}

void gen_e(int*e, int g, int x_secret, int p){
    *e = cpow_mod(g, x_secret, p);
}

void gen_e_L(long long*e, long long g, long long x_secret, long long p){
    *e = cpow_mod(g, x_secret, p);
}

void gen_keys(int* g, int x_secret, int* e, int p){
    gen_g(g, p);
    gen_e(e, *g, x_secret, p);
}

void gen_keys_FAST(int* g, int x_secret, int* e, int p){
    gen_g_FAST(g, p);
    gen_e(e, *g, x_secret, p);
}

void gen_keys_FASTEST(long long* g, long long x_secret, long long* e, long long p){
    gen_g_FASTEST(g, p);
    gen_e_L(e, *g, x_secret, p);
}


void str_int(int* intgr, char* str, int str_len){

    for (int i = 0; i<str_len; i++){
        intgr[i] = (int) str[i];
    }

}

void int_str(char* str, int* intgr, int str_len){

    for (int i = 0; i<str_len; i++){
        str[i] =  intgr[i];
    }
}

void encrypt_str(int* str_encrpt, int* str_int, int secret, int e, int p, int str_len){
    for(int i=0; i<str_len; i++){
        str_encrpt[i] = ((str_int[i]%p) * cpow_mod(e, secret, p)) % p;
    }
}

void decrpyt_str(char* str_decrpt, int* str_encrpt, int secret, int p, int str_len){

    int i;
    // printf("x_key: %d p: %d\n", secret, p);
    for (i = 0; i<str_len; i++){
        // printf("ge %d\n", ((str_encrpt[i] % p) * cpow_mod(secret, p-2, p)) % p);
        str_decrpt[i] = ((str_encrpt[i] % p) * cpow_mod(secret, p-2, p)) % p;
    }
    str_decrpt[i] = '\0';
}

int main(){

    clock_t t;
    t = clock();
    
    long long p = 4000000007;
    
    int count =0;
    // for (int i =1; i < p; i++)
    // {
    //     if (cis_primitive_root(i, p)){
    //         count++;
    //         // printf("%d Is primitive root to %d\n", i, p);   
    //     }
    // }
    // int g___ = generator(p); printf("g him: %d\n", g___);
    int g_GLOBAL_ = cget_first_primitive_root_loop(p); printf("g  my: %d\n", g_GLOBAL_);  // generate g //

    t = clock() - t;
    double time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds
 
    printf("took %f seconds to execute \n", time_taken);
    printf("number of primitive roots: %d\n", count);

    return 0;

    int p_GLOBAL = 1009;  // Any large prime //
    int g_GLOBAL = cget_first_primitive_root_loop(p_GLOBAL);  // generate g //
    int g__ = generator(p_GLOBAL);
    printf("g: %d\ng: %d\n", g_GLOBAL, g__);

    int x_random_SECRET = rand() % (p_GLOBAL-2) + 1;  // My Secret key //
    x_random_SECRET = 54;

    int e_GLOBAL = cpow_mod(g_GLOBAL, x_random_SECRET, p_GLOBAL); // Global e //

    gen_keys(&g_GLOBAL, x_random_SECRET, &e_GLOBAL, p_GLOBAL);

    printf("g %d\n", g_GLOBAL);
    printf("e %d\n", e_GLOBAL);
// ########################################################### 
// ########### Transfare(e, g, p) to bob #####################
// ########################################################### 

    int y_random_SECRET =rand() % (p_GLOBAL-2) + 1;   // His random secret key //

    y_random_SECRET = 43;

    char* message = "Hi Alice!"; // Bob's message to me! //
    int s = strlen(message);
    printf("message: %s\n", message);

    // Computing cypher message c1, c2[] //
    int* message_encrtpted = calloc(strlen(message), sizeof(int));
    


    str_int(message_encrtpted, message, s);


    //   msg * e^y  mod p
    //  msg mod p * e

    int* c2 = calloc(1+strlen(message), sizeof(int));

    for(int i=0; i<strlen(message); i++){
        c2[i] = ((message_encrtpted[i]%p_GLOBAL) * cpow_mod(e_GLOBAL, y_random_SECRET, p_GLOBAL)) % p_GLOBAL;
    }
        
    encrypt_str(c2, message_encrtpted, y_random_SECRET, e_GLOBAL, p_GLOBAL, strlen(message));

    int c1 = generate_c1(g_GLOBAL, y_random_SECRET, p_GLOBAL);
// ########################################################### 
// ######### Bob Transfare(c1, c2, strlen(message)) to me ####
// ########################################################### 


    int x = cpow_mod(c1, x_random_SECRET, p_GLOBAL);

    char* decrypted_message = calloc(1+strlen(message), sizeof(char));
    
    int i;
    for (i = 0; i<strlen(message); i++){

        decrypted_message[i] = ((c2[i]%p_GLOBAL) * cpow_mod(x, p_GLOBAL-2, p_GLOBAL)) % p_GLOBAL;
        }
    decrypted_message[i] = '\0';

    decrpyt_str(decrypted_message, c2, x, p_GLOBAL, strlen(message));
    
    // char* decr_str = calloc(1+strlen(message), sizeof(char));

    // int_str(decr_str, decrypted_message, strlen(message));
    // printf("len %d\n", (int)strlen(decrypted_message));

    printf("plain:   %s\n", decrypted_message);

    return 0;

}


/*
###########################################################
            Py module stuff
###########################################################
*/
#if 1

static PyObject* is_prime(PyObject* self, PyObject* args){
    long long number;
    int sts;
    if (!PyArg_ParseTuple(args, "L", &number))
        return NULL;
    
    sts = cis_prime(number);

    return PyBool_FromLong(sts);
}

static PyObject* gen_keys_p(PyObject* self, PyObject* args){
    int p, secret, g_, e_;
    
    if (!PyArg_ParseTuple(args, "ii", &p, &secret))
        return NULL;
    
    gen_keys(&g_, secret, &e_, p);
    
    PyObject* sts = PyTuple_Pack(2, PyLong_FromLong(g_),  PyLong_FromLong(e_));

    return sts;
}

static PyObject* gen_keys_FAST_p(PyObject* self, PyObject* args){
    int p, secret, g_, e_;
    
    if (!PyArg_ParseTuple(args, "ii", &p, &secret))
        return NULL;
    
    gen_keys_FAST(&g_, secret, &e_, p);
    PyObject* sts = PyTuple_Pack(2, PyLong_FromLong(g_),  PyLong_FromLong(e_));

    return sts;
}

static PyObject* gen_keys_FASTEST_p(PyObject* self, PyObject* args){
    long long p, secret, g_, e_;
    
    if (!PyArg_ParseTuple(args, "LL", &p, &secret))
        return NULL;
    
    gen_keys_FASTEST(&g_, secret, &e_, p);
    PyObject* sts = PyTuple_Pack(2, PyLong_FromLongLong(g_),  PyLong_FromLongLong(e_));

    return sts;
}

static PyObject* gen_c1_p(PyObject* self, PyObject* args){
    int  p, secret, g, sts;
    if (!PyArg_ParseTuple(args, "iii", &g, &secret, &p))
        return NULL;
    
    sts = cpow_mod(g, secret, p);
    return PyLong_FromLong(sts);
}

static PyObject* gen_x_key_py(PyObject* self, PyObject* args){
    int c1, secret, p, sts;

    if (!PyArg_ParseTuple(args, "iii", &c1, &secret, &p))
        return NULL;
    
    sts = cpow_mod(c1, secret, p);
    return PyLong_FromLong(sts);
}

static PyObject* encrypt_p(PyObject* self, PyObject* args){
    char* msg;
    int p, secret, e;
    if (!PyArg_ParseTuple(args, "siii", &msg, &secret, &e, &p))
        return NULL;

    int str_ = strlen(msg);
    int* intgr =  malloc(str_ * sizeof(int));
    int* encr =  malloc(str_ * sizeof(int));
    
    str_int(intgr, msg, str_);

    encrypt_str(encr, intgr, secret, e, p, str_);

    PyObject* list_out = PyList_New(0);

    for(int i=0;i<str_;i++){
        PyList_Append(list_out, PyLong_FromLong(encr[i]));        
    }

    free(encr);
    free(intgr);
    return list_out;
}

static PyObject* decrypt_p(PyObject* self, PyObject* args){
    int p, x_key, len_msg = _PyLong_AsInt(PyNumber_Long(PyTuple_GetItem(args, 0)));

    int* encr =  malloc(1+len_msg * sizeof(int));

    int i;
    for(i=0;i<len_msg;i++){
        encr[i] = _PyLong_AsInt(PyNumber_Long(PyTuple_GetItem(args, i+1))); 
    }

    x_key = _PyLong_AsInt(PyNumber_Long(PyTuple_GetItem(args, ++i)));
    p = _PyLong_AsInt(PyNumber_Long(PyTuple_GetItem(args, ++i)));

    char* decrypted_message = malloc(2+len_msg* sizeof(char));
    
    decrpyt_str(decrypted_message, encr, x_key, p, len_msg-1);

    return Py_BuildValue("s", decrypted_message);;
}

static PyObject* version(PyObject* self){
    return Py_BuildValue("s", "Version 0.2.6");
}

static PyMethodDef ElGamal_cs[] = {
    {"is_prime", is_prime, METH_VARARGS, "Calculates if the number is prime or not."},
    {"gen_keys", gen_keys_p, METH_VARARGS, "generates keys"},
    {"gen_keys_FAST", gen_keys_FAST_p, METH_VARARGS, "generates keys, but Fast"},
    {"gen_keys_FASTEST", gen_keys_FASTEST_p, METH_VARARGS, "generates keys, but so much Fast"},
    {"gen_c1", gen_c1_p, METH_VARARGS, "generate cypher text 1"},
    {"gen_x_key", gen_x_key_py, METH_VARARGS, "generate x_key for decryption"},
    {"encrypt", encrypt_p, METH_VARARGS, "encrypt message"},
    {"decrypt", decrypt_p, METH_VARARGS, "decrypt c1, c2 cypher messages"},
    {"version", (PyCFunction)version, METH_NOARGS, "Returns the version of the module."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef ElGamal_c = {
    PyModuleDef_HEAD_INIT,
    "ElGamal_c",
    "Prime calculations module",
    -1, // global state
    ElGamal_cs,
};

PyMODINIT_FUNC PyInit_ElGamal_c(void)
{
    return PyModule_Create(&ElGamal_c);   
}


#endif