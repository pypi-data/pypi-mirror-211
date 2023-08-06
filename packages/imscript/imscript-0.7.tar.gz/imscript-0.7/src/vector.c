// simple vector graphics stuff

enum {
	VECTOR_NOTHING,
	VECTOR_DOT,
	VECTOR_SEGMENT,
	VECTOR_POLYGON,
	VECTOR_CIRCLE,
	VECTOR_ELLIPSE,
	VECTOR_LABEL,
};

struct vector_graphics {
	int n; // number of objects
	int *types;
	void **data;
};

struct vector_add_object(
		struct vector_graphics *v,   // the list of objects
		int t,                       // type of the new object
		int s,                       // data size
		void *d                      // data
		)
{
	v->n += 1;

}
