#include <stdio.h> // only for "fprintf"
#include <stdlib.h> // only for "free"
#include <stdint.h>
#include "iio.h"

// read an image in any format from STDIN and write a ppm to STDOUT
int main_iionint(int c, char *v[])
{
	if (c != 3)
		return fprintf(stderr, "usage:\n\t%s infile outfile\n", *v);
	//                                         0 1      2
	char *filename_in = v[1];
	char *filename_out = v[2];
	int w, h;
	int *x = iio_read_image_int(filename_in, &w, &h);
	iio_write_image_int(filename_out, x, w, h);
	free(x);
	return 0;
}
#ifndef HIDE_ALL_MAINS
int main(int c, char **v) { return main_iionint(c, v); }
#endif
