#ifndef phylib_h
#define phylib_h

// CONSTANTS//
#define PHYLIB_BALL_RADIUS (28.5) // mm
#define PHYLIB_BALL_DIAMETER (2*PHYLIB_BALL_RADIUS)
#define PHYLIB_HOLE_RADIUS (2*PHYLIB_BALL_DIAMETER)
#define PHYLIB_TABLE_LENGTH (2700.0) // mm
#define PHYLIB_TABLE_WIDTH (PHYLIB_TABLE_LENGTH/2.0) // mm
#define PHYLIB_SIM_RATE (0.0001) // s
#define PHYLIB_VEL_EPSILON (0.01) // mm/s
#define PHYLIB_DRAG (150.0) //mm/s^2
#define PHYLIB_MAX_TIME (600.0) // s  
#define PHYLIB_MAX_OBJECTS (26)

// POLYMORPHIC OBJECT TYPES//
typedef enum {
    PHYLIB_STILL_BALL = 0,
    PHYLIB_ROLLING_BALL = 1,
    PHYLIB_HOLE = 2,
    PHYLIB_HCUSHION = 3,
    PHYLIB_VCUSHION = 4,
} phylib_obj;

// 2 DIMENSIONAL VECTOR CLASS//
typedef struct {
    double x;
    double y;
} phylib_coord;

// CHILD CLASSES//

// Ball not in motion//
typedef struct {
    unsigned char number;
    phylib_coord pos;
} phylib_still_ball;

// ROLLING BALL//

typedef struct {
    unsigned char number;
    phylib_coord pos;
    phylib_coord vel;
    phylib_coord acc;
} phylib_rolling_ball;

// 6 Holes on the table//

typedef struct {
    phylib_coord pos;
} phylib_hole;

// HORIZONTAL CUSHION//

typedef struct {
    double y;
} phylib_hcushion;

// Vertical Cushion//
typedef struct {
double x;
} phylib_vcushion;

// Polymorphic Parent Class of objects//
typedef union {
    phylib_still_ball still_ball;
    phylib_rolling_ball rolling_ball;
    phylib_hole hole;
    phylib_hcushion hcushion;
    phylib_vcushion vcushion;
} phylib_untyped;

// TO IDENTIFY WHAT CLASS OF THE OBJECT IS//
typedef struct {
    phylib_obj type;
    phylib_untyped obj;
} phylib_object;

// THE TABLE//

typedef struct {
double time;
phylib_object *object[PHYLIB_MAX_OBJECTS];
} phylib_table;

// FUNCTION PROTOTYPES //

/*This function will allocate memory for a new phylib_object, set its type to
PHYLIB_STILL_BALL and transfer the information provided in the function parameters into the
structure. It will return a pointer to the phylib_object. If the malloc function fails, it will
return NULL (before trying to store the function parameters in the (non-existent) structure).*/

phylib_object *phylib_new_still_ball( unsigned char number, phylib_coord *pos );

/*These functions will do the same thing as the phylib_new_still_ball function for their
respective structures.*/

phylib_object *phylib_new_rolling_ball( unsigned char number,
phylib_coord *pos,
phylib_coord *vel,
phylib_coord *acc);

phylib_object *phylib_new_hole( phylib_coord *pos );
phylib_object *phylib_new_hcushion( double y );
phylib_object *phylib_new_vcushion( double x );

/*This function will allocate memory for a table structure, returning NULL if the memory
allocation fails. The member variable, time, will be set to 0.0. It will then assign the values of
its array elements to pointers to new objects created by the phylib_new_* functions provided
above. Specifically, it will add elements in this order:
1) a horizontal cushion at y=0.0;
2) a horizontal cushion at y=PHYLIB_TABLE_LENGTH;
3) a vertical cushion at x=0.0;
4) a vertical cushion at x=PHYLIB_TABLE_WIDTH;
5) 6 holes: positioned in the four corners where the cushions meet and two more
midway between the top holes and bottom holes.
The remaining pointers will all be set to NULL.
*/

phylib_table *phylib_new_table( void );

// UTILITY FUNCTIONS//


void phylib_copy_object( phylib_object **dest, phylib_object **src );
/*This function should allocate new memory for a phylib_object. Save the address of that
object at the location pointed to by dest, and copy over the contents of the object from the
location pointed to by src. Hint, you can use memcpy to make this a one-step operation that
works for any type of phylib_object. If src points to a location containing a NULL pointer,
then the location pointed to by dest should be assigned the value of NULL.*/

phylib_table *phylib_copy_table( phylib_table *table);
/*This function should allocate memory for a new phylib_table, returning NULL if the malloc
fails. Then the contents pointed to by table should be copied to the new memory location and
the address returned*/

void phylib_add_object( phylib_table *table, phylib_object *object);

/*This function should iterate over the object array in the table until it finds a NULL pointer. It
should then assign that pointer to be equal to the address of object. If there are no NULL
pointers in the array, the function should do nothing.*/

void phylib_free_table( phylib_table *table );

/*This function should free every non- NULL pointer in the object array of table. It should then
also free table as well.*/


phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 );

/*This function should return the difference between c1 and c2. That is the result’s x value
should be c1.x-c2.x and similarly for y*/

double phylib_length( phylib_coord c);
/*This function should return the length of the vector/coordinate c*/

 double phylib_dot_product( phylib_coord a, phylib_coord b);
/*This function should compute the dot-product between two vectors*/


 double phylib_distance( phylib_object *obj1, phylib_object *obj2 );
 /*This function should calculate the distance between two objects, obj1 and obj2.*/


 // FUNCTIONS FOR SIMULATING BALLS MOVING ??

 void phylib_roll( phylib_object *new, phylib_object *old, double time );
 /*This function updates a new phylib_object that represents the old phylib_object after it
has rolled for a period of time. If new and old are not PHYLIB_ROLLING_BALLs, then the
function should do nothing. Otherwise, it should update the values in new. Specifically the
position, and velocities should be updated as follows:
*/

unsigned char phylib_stopped( phylib_object *object );
/*This function will check whether a ROLLING_BALL has stopped, and if it has, will convert it to a
STILL_BALL. You may assume that object is a ROLLING_BALL. The function will return 1 if it
converts the ball, 0 if it does not.
For the purposes of this simulation a ball is considered to have stopped if its speed (which is the
length of its velocity) is less than PHYLIB_VEL_EPSILON.
Do not assume that the number, and x and y positions of the rolling ball will be automatically
transferred to the still ball.
*/
 
 void phylib_bounce( phylib_object **a, phylib_object **b );
 /**/

 unsigned char phylib_rolling( phylib_table *t );
//This function should return the number of ROLLING_BALLS on the table.

 phylib_table *phylib_segment( phylib_table *table );
 /**/

double phylib_square( double cx);
double poseq( double pos, double veloc, double accel, double time);
double veleq(double vel, double accel, double time);

char *phylib_object_string(phylib_object *object);

#endif
