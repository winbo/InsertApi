#ifndef C_H
#define C_H

#ifdef __cplusplus
extern "C" {
#endif


const void *
memcpy (
	void *dst, 
	const void *src, 
	size_t size);    

long  strtol ( const char *str)		;
int   qsort( void *array, size_t item_size, size_t item_count, int (* compare)(void *a, void *b));
#define swap(a, b)  \
	do { \
		typeof(a) _tmp = (a); \
		(a) = (b); \
		(b) = _tmp; \
		} \
		while(0)

   #  define max(a, b)

#define 	min(a, b)   

#define  PI    (3.1415926)

#define tty_locked()		(current == __big_tty_mutex_owner)
extern int send_indication(int id, const char *fmt, ...);
int send_request(int id, const char *fmt, ...); // send request
int send_response(int id, const char *fmt, ...);
int (*acpi_op_add) (struct acpi_device * device);
int register_acpi_bus_type(struct acpi_bus_type *);
int acpi_pm_device_sleep_wake(struct device *, bool);
struct record & get_record(void);
union status* get_status();

static inline struct cryptd_ablkcipher *__cryptd_ablkcipher_cast(
	struct crypto_ablkcipher *tfm)
{
	if (tfm) {
		return (struct cryptd_ablkcipher *)tfm;
	} else {
		return NULL;
	}
}

/* interface */
/*
int at_exec(const char *cmd, int length);
int at_register_handle(const char *prefix, int length);
*/

// int at_unregister_handle(int id);
	// 		this is comment.

/**
 * int main(int argc, char const *argv[])
 */

/** } */
 
#ifdef __cplusplus
}
#endif

#endif