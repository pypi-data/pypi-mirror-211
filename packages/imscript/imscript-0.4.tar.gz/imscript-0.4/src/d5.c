// d5 : dense 5-dimensional tiled arrays

struct d5_array {
	long s[5];   // size of each dimension
	long t[5];   // tile size
	float *x;
};
