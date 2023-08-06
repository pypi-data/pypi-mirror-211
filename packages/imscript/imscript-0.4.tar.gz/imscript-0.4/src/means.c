static float float_scalar_weighted_avg(float *w, float *x, int n)
{
	long double a = 0;
	long double b = 0;
	for (int i = 0; i < n; i++)
	{
		a += w[i] * x[i];
		b += w[i];
	}
	return a / b;
}
