#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>

typedef struct Matrix{
int size[2];
double** matrix;
} Matrix;

typedef struct Vec{
int lenght;
double* vec;
}Vec;

typedef void (*l_func_)(Vec*, Vec*);

typedef struct L_func_{
l_func_ Func;
l_func_ d_Func;
}L_func_;

typedef void (d_func_)(Vec*,Vec*,Vec*);

typedef struct D_func{
d_func_ Dist;
d_func_ d_Dist;
} D_func;

typedef struct Layer{
Vec *out;
Vec *Bias;
Matrix *Weights;
L_func_ *L_func;
}

typedef struct Graph{
int depth;
Vec *in;
Layer **layers;
int* l_neurons;
}Graph;

//non-core functions
double randn (double mu, double sigma){ // standard implementation - copied from phoxis.org
  double U1, U2, W, mult;
  static double X1, X2;
  static int call = 0;

  if (call == 1)
    {
      call = !call;
      return (mu + sigma * (double) X2);
    }

  do
    {
      U1 = -1 + ((double) rand () / RAND_MAX) * 2;
      U2 = -1 + ((double) rand () / RAND_MAX) * 2;
      W = pow (U1, 2) + pow (U2, 2);
    }
  while (W >= 1 || W == 0);

  mult = sqrt ((-2 * log (W)) / W);
  X1 = U1 * mult;
  X2 = U2 * mult;

  call = !call;

  return (mu + sigma * (double) X1);
}

void MatMul(Matrix *mat, Vec *x, Vec *out){//out = mat*x
int i,j;
for (i=0;i<out->lenght;i++){
    out->*(vec+i) =0;
}
for (i=0;i<mat->size[0];i++){
    for (j=0;j<mat->size[1];j++){
        out->*(vec+i) += mat->*(*(matrix+i)+j) * x->*(vec+j)
    }
}
}

void Vec_point_sum(Vec *x, Vec *b, Vec *out){// out[i]=v[i]+b[i]
int i;

for (i=0; i<x->lenght;i++){
    out->*(vec+i)=b->*(vec+i)+v->*(vec+i);
}
}

void Mat_point_sum(Matrix *A, Matrix *B, Matrix *Out){// Out[i][j]=A[i][j]+B[i][j]
int i,j;

for(i=0;i<A->size[0];i++){
    for(j=0;j<A->size[1],j++){
       Out->*(*(matrix+i)+j)=A->*(*(matrix+i)+j)+B->*(*(matrix+i)+j)
    }
}
}

void Vec_point_mlt(Vec* x, Vec *y, Vec *out){// out[i]=x[i]*y[i]
int i;

for(i=0;i<x->lenght;i++) {out->*(vec+i)=x->*(vec+i) * (y->*(vec+i));}
}

void Vec_const_mlt(Vec *x, double c, Vec *out){// out[i]=c*x[i]
int i;

for(i=0;i<x->lenght;i++){out->*(vec+i) =x->*(vec+i) * c;}
}

void Transpose(Matrix *A, Matrix *AT){// AT=A^T
    int i,j;

    for(i=0;i<AT->size[0];i++){
            for(j=0;j<AT->size[1];j++){
                AT->*(*(matrix+i)+j)=A->*(*(matrix+j)+i);
            }
        }

}

int *invert_table(int *t){
int i,d=sizeof(t)/sizeof(int);

int *tmp=(int*)malloc(sizeof(int)*d);
for(i=0;i<d;i++){*(tmp+i)=*(t+d-i-1);}

return tmp;
}
//non-core functions

void Relu(Vec *in ,Vec *out){
int i;

for (i=0;i<in->lenght;i++){
    if (in->*(vec+i)<0) out->*(vec+i)=0;
    else out->*(vec+i)= in->*(vec+i);
}
}

void d_Relu(Vec *in,Vec *out){
int i;
for (i=0;i<in->lenght;i++){
    if (in->*(vec+i)<0) out->*(vec+i)=0;
    else out->*(vec+i)=1;
}
}

void identity(Vec *in,Vec *out){
int i;
for (i=0;i<in->lenght;i++){
    out->*(vec+i)= in->*(vec+i)
}
}

void d_identity(Vec *in,Vec *out){
int i;
for (i=0;i<in->lenght;i++){
    out->*(vec+i)=1;
}
}

void distance2(Vec *v1, Vec *v2, Vec *dist){//
int i;
double tmp;

for(i=0;i<v1->lenght;i++){tmp+=(v1->*(vec+i) - v2->*(vec+i))*(v1->*(vec+i) - v2->*(vec+i))/(v1->lenght);}
dist->*vec=tmp;
}

void d_distance2(Vec *v1, Vec *v2, Vec *d_dist){//d_dist[i]= - d distance_2/d v1[i]  //v2 ~data
int i;
for(i=0;i<v1->lenght;i++){d_dist->*(vec+i) = -1*(v1->*(vec+i) - v2->*(vec+i))*2/(v1->lenght);}
}

Matrix *init_matrix(int n, int m){
    int i,j;

    Matrix *mat=(Matrix*)malloc(sizeof(Matrix))
    mat->size[0]=n;
    mat->size[1]=m;
    mat->matrix=(double**)malloc(sizeof(double*)*n);
    for (i=0;i<n;i++){mat->*(matrix+i)=(double*)malloc(sizeof(double)*m);}
    for(i=0;i<n;i++){
        for(j=0;j<m;j++){
            mat->*(*(matrix+i)+j)=randn(0,0.05);
        }
    }
    return mat;
}//add reality check and free space IC alloc error

void clear_Matrix(Matrix *mat){
int i,j;

for(i=0;i<mat->size[0];i++){
    for(j=0;j<mat->size[1];j++){
         mat->*(*(matrix+i)+j)=0;
    }
}
}

Vec *init_vec(int n){
int i;

Vec *v=(Vec*)malloc(sizeof(Vec));
v->vec=(double*)malloc(sizeof(double)*n);
v->lenght = n;

for(i=0;i<n;i++){
    v->*(vec+i)=randn(0,1);
}
return v;
}//add reality check and free space IC alloc error

void clear_Vec(Vec *v){
int i;

for(i=0;i<v->lenght;i++){v->*(vec+i)=0;}
}

int build_Graph(Graph *g, int *neurons){ //neurons should be passed into the main(), same as list of activation functions - TBI; neurons[0] = in; neurons[-1] = out;
int i;

g = (Graph*)malloc(sizeof(Graph));
if(!g) return 0;
g->depth = sizeof(neurons)/sizeof(int);
g->l_neurons = (int*)malloc(sizeof(int)*(g->depth));
if(!l_neurons) return 0;
for(i=0;i<g->depth;i++){*(l_neurons+i)=neurons[i];}
g->layers = (Layer**)malloc(sizeof(Layer*)*(g->depth-1));
if(!layers) return 0;

for (i=0;i<(g->depth-1);i++){
    g->*(layers+i)=(Layer*)malloc(sizeof(Layer));
    if(!(g->*(layers+i))) return 0;
    g->*(layers+i)->L_func = (L_func_*)malloc(sizeof(L_func_));
    if(!(g->*(layers+i)->L_func)) return 0;

    g->*(layers+i)->out= init_vec(*(neurons+1+i));
    if(!(g->*(layers+i)->out)) return 0;
    g->*(layers+i)->Bias= init_vec(*(neurons+1+i));
    if(!(g->*(layers+i)->Bias)) return 0;
    g->*(layers+i)->Weights = init_matrix(*(neurons+i),*(neurons+1+i))
    if(!(g->*(layers+i)->Weights)) return 0;

    if(i==(g->depth) -2){
    g->*(layers+i)->L_func->Func = &identity;
    g->*(layers+i)->L_func->d_Func = &d_indentity;
    }
    else{
    g->*(layers+i)->L_func->Func = &Relu;
    g->*(layers+i)->L_func->d_Func = &d_Relu;
    }
}//declaring each layer

g->in = init_vec(neurons[0]);
if(!(g->in)) return 0;

return 1;
}//add reality check and free space IC alloc error

int build_d_Graph(Graph *d_g_itr, Graph *g){
int i, ctrl;
if(!g) return 0;
int *inv_neurons = invert_table(g->l_neurons);

ctrl = build_Graph(d_g_itr, inv_neurons);
if (!ctrl) return 0;
for(i=0;i<d_g_itr->depth-1;i++){
    d_g_itr->*(layer+i)->L_func->Func=g->*(layer+g->depth-1-i)->L_func->Func;
    d_g_itr->*(layer+i)->L_func->d_Func=g->*(layer+g->depth-1-i)->L_func->d_Func;
}
free(inv_neurons);
return 1;
}

void clear_Graph(Graph *g){
int i;

for (i=0;i<(g->depth)-1;i++){

    clear_Vec(g->(layers+i)->out);
    clear_Vec(g->(layers+i)->Bias);
    clear_Matrix(g->(layers+i)->Weights);
}

clear_Vec(g->in);
}

void Train_on_batch(Graph *g, Graph *d_g_itr, Graph *d_g, double **data, double lambda, D_Func dist){
int i,j,k,l;

if(!g){puts(puts("Computational Graph missing");system("PAUSE");return;)}
if(!d_g_itr){puts(puts("Gradient Graph missing");system("PAUSE");return;)}
if(!d_g_itr){puts(puts("Cumulative gradient Graph missing");system("PAUSE");return;)}
if(!data){puts("Training lacks data");system("PAUSE");return;}
if(!lambda){puts("Learning rate missing or 0");system("PAUSE");return;}


int batch_size = sizeof(data)/sizeof(double*);
int data_vec_lenght = sizeof(*data)/sizeof(double);
int n_layers = g->depth -1;

Vec **aux_vecs = (Vec**)malloc(sizeof(Vec*)*(n_layers);
clear_Graph(d_g);
for(j=0;j<n_layers;j++){
    *(aux_vecs+j)=(Vec*)malloc(sizeof(Vec));
    *(aux_vecs+j)->vec=(double*)malloc(sizeof(doulbe)*(d_g_itr->*(l_neurons+1+j));
    *(aux_vecs+j)->lenght=d_g_itr->*(l_neurons+1+j);
}// creating aux vectors

for(j=0;j<n_layers;j++){Transpose(g->*(layers+j)->Weights, g->*(layers+n_layers-j-1)->Weights);}
 // updating Weights in d_g_itr
for(i=0;i<batch_size;i++){//single data vector

    //forward pass
    identity(*(data+i),g->in)// for(j=0; j<g->*l_neurons;j++){g->*(in+j)=*(*(data+i)+j);}
    for(j=0;j<n_layers;j++){

        if(j==0){Matmul(g->*(layers+j)->Weights, in, g->*(layers+j)->out);}
        else {Matmul(g->*(layers+j)->Weights, g->*(layers+j-1)->out, g->*(layers+j)->out);}

        vec_point_sum(g->*(layers+j)->out, g->*(layers+j)->Bias, g->*(layers+j)->out);
        (g->*(layers+j)->L_Func->*Func)(g->*(layers+j)->out,g->*(layers+j)->out);
    }//forward pass

    //back pass
    (dist->*d_Dist)(g->*(layers+n_layers-1)->out,*(data+i)+data_vec_lenght-(d_g_itr->*l_neurons)-1,d_g_itr->in);
    for(j=0;j<n_layers;j++){
        (d_g_itr->*(layers+j)->L_Func->*d_Func)(g->*(layers+n_layers-1-j)->out,*(aux_vecs+j));

        if (j==0){
            Vec_point_mlt(d_g_itr->in, *(aux_vecs+j),d_g_itr->in);

            Vec_const_mlt(d_g_itr->in, lambda/batch_size, d_g_itr->*(layers+j)->Bias);
            Vec_point_sum(d_g->*(layers+n_layers-1-j)->Bias, d_g_itr->*(layers+j)->Bias, d_g->*(layers+n_layers-1-j)->Bias);

            Matmul(d_g_itr->*(layers+j)->Weights, d_g_itr->in, d_g_itr->*(layers+j)->out);

        }
        else {
            Vec_point_mlt(d_g_itr->*(layers+j-1)->out, *(aux_vecs+j), d_g_itr->*(layers+j-1)->out);

            Vec_const_mlt(d_g_itr->*(layers+j-1)->out, lambda/batch_size, d_g_itr->*(layers+j)->Bias);
            Vec_point_sum(d_g->*(layers+n_layers-1-j)->Bias, d_g_itr->*(layers+j)->Bias, d_g->*(layers+n_layers-1-j)->Bias);

            Matmul(d_g_itr->*(layers+j)->Weights, d_g_itr->*(layers+j-1)->out, d_g_itr->*(layers+j)->out);

        }


        for(k=0;k<g->*(l_neurons+n_layers-1-j);k++){
            if(n_layers-2-j==-1){Vec_const_mlt(g->in, (d_g_itr->*(layers+j-1)->out->*(vec+k))*lambda/batch_size, *(aux_vecs+j);}
            else {Vec_const_mlt(g->*(layers+n_layers-2-j)->out, (d_g_itr->*(layers+j-1)->out->*(vec+k))*lambda/batch_size, *(aux_vecs+j);}
            for(l=0;l<d_g->*(layers+n_layers-1-j)->Weights->size[0];l++){d_g->*(layers+n_layers-1-j)->Weights->*(*(matrix+k)+l)+=*(aux_vec+j)->*(vec+l);}
        }
    }//back pass
}//single data vector

for(j=0;j<n_layers;j++){//update parameters
    Vec_point_sum(g->*(layers+j)->Bias, d_g->*(layers)->Bias, g->*(layers+j)->Bias);
    Mat_point_sum(g->*(layers+j)->Weights, d_g->*(layers)->Weights, g->*(layers+j)->Weights);
}//update parameters


for(j=0;j<(d_g_itr->depth);j++){
    free(*(aux_vecs+j)->vec);
    free(*(aux_vecs+j));
}free(aux_vecs);//freeing aux vectors


}



int main(){

}
