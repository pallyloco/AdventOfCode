#!/usr/bin/perl
use strict;
use warnings;
my $short = shift || 0;

my @program   = <DATA>;
my $model_num = "2359246899999";

#             12345678901234
$model_num = "11211791117965";
my $input = [ split "", $model_num ];

# validate the rules
###########################################################################3
# Rules for 'x' to be zero
############################################################################
#  w4 =  w3 - 1 (step 4)     x
#  w6 =  w5 + 6 (step 6)     x
#  w7 =  w2 + 8 (step 7)     x
#  w9 =  w8     (step 9)     x
# w12 = w11 + 2 (step 12)    x
# w13 = w10 + 5 (step 13)
# w14 =  w1 + 4 (step 14)    x

# Smallest Number
# 12345678901234
# 1            5    # w14 = w1 + 4
# 11    9      5    # w7 = w2 + 8
# 1121  9      5    # w4 = w3 - 1
# 1121179      5    # w6 = w5 + 6
# 112117911    5    # w9 = w8
# 112117911 13 5    # w12 = w11 + 2
# 11211791111365    # w13 = w10 + 5

# 11211791111365




# Largest Number
# 12345678901234
# 5            9    # w14 = w1 + 4
# 51    9      9    # w7 = w2 + 8
# 5198  9      9    # w4 = w3 - 1
# 5198399      9    # w6 = w5 + 6
# 519839999    9    # w9 = w8
# 519839999 79 9    # w12 = w11 + 2
# 51983999947999    # w13 = w10 + 5


    # cumulative
    # step 1        z =        (w1 + 6)
    # step 2        z =     26*(w1 + 6) + w2 + 14
    # step 3        z = 26*(26*(w1 + 6) + w2 + 14) + (w3 + 13)
    # step 4        z =     26*(w1 + 6) + w2 + 14               if  w4 =  w3 - 1 
    # step 5        z = 26*(26*(w1 + 6) + w2 + 14) + (w5 + 6)
    # step 6        z =     26*(w1 + 6) + w2 + 14               if  w6 =  w5 + 6
    # step 7        z =        (w1 + 6)                         if  w7 =  w2 + 8
    # step 8        z =     26*(w1 + 6) + w8 + 3
    # step 9        z =        (w1 + 6)                         if  w9 =  w8
    # step 10       z =     26*(w1 + 6) + w10 + 14
    # step 11       z = 26*(26*(w1 + 6) + w10 + 14) + $w11 + 4
    # step 12       z =     26*(w1 + 6) + w10 + 14              if w12 = w11 + 2
    # step 13       z =         w1 + 6                          if w13 = w10 + 5
    # step 14       z =            0                            if w14 =  w1 + 4


short($input);

sub short {
    my $input = shift;
    my ( $w, $x, $y, $z ) = ( 0, 0, 0, 0 );

    # cumulative
    # step 1        (26^0)
    print @$input, "\n";
    $w = shift @$input;
    my $w1 = $w;
    $x = 1;
    $y = $w + 6;
    $z = $w + 6;    # z = w1 + 6
    print "Testing: $z = ", $w1 + 6, "\n";
    print "Step  1\t($w, $x, $y, $z)\n";

    # step 2        (26^1)
    $w = shift @$input;
    my $w2 = $w;
    $x = 1;
    $y = $w + 14;
    $z = 26 * $z + $y;    # z = 26*(w1 + 6) + w2 + 14
    print "Testing: $z = ", 26 * ( $w1 + 6 ) + $w2 + 14, "\n";
    print "Step  2\t($w, $x, $y, $z)\n";

    # step 3
    $w = shift @$input;    # z = 26*(26*(w1 + 6) + w2 + 14) + (w3 + 13)
    my $w3 = $w;
    $x = 1;
    $y = $w + 13;
    $z = 26 * $z + $y;
    print "Testing: $z = ", 26 * ( 26 * ( $w1 + 6 ) + $w2 + 14 ) + $w3 + 13,
      "\n";
    print "Step  3\t($w, $x, $y, $z)\n";

    # step 4
    $w = shift @$input;
    my $w4 = $w;
    $x = $z % 26;                # want x to be zero, (w3+13-14) = w4
    $z = int( $z / 26 );         # ********** w4 = w3-1 *******
    $x = $x - 14;                #
    $x = int( $x != $w );
    $y = 25 * $x + 1;
    $z = $z * ( 25 * $x + 1 );
    $y = ( $w + 1 ) * $x;
    $z = $z + $y;                # z = 26*(w1 + 6) + w2 + 14
    print "Testing: $z = ", 26 * ( $w1 + 6 ) + $w2 + 14, "\n";
    print "Step  4\t($w, $x, $y, $z)\n";

    # step 5
    $w = shift @$input;
    my $w5 = $w;
    $x = 1;
    $y = $w + 6;
    $z = 26 * $z + $w + 6;       # z = 26*(26*(w1 + 6) + w2 + 14) + (w5+6)
    print "Testing: $z = ", 26 * ( 26 * ( $w1 + 6 ) + $w2 + 14 ) + $w5 + 6,
      "\n";
    print "Step  5\t($w, $x, $y, $z) \n";

    # step 6
    $w = shift @$input;          # want x to be zero
    my $w6 = $w;
    $x = $z % 26;                    # ***** w5+6 = w6 *****
    $z = int( $z / 26 );             #
    $x = int( $x != $w );
    $z = ( ( 25 * $x ) + 1 ) * $z;
    $y = ( $w + 13 ) * $x;
    $z = $z + ( $w + 13 ) * $x;      # z = 26*(w1 + 6) + w2 + 14
    print "Testing: $z = ", ( 26 * ( $w1 + 6 ) + $w2 + 14 ), "\n";
    print "Step  6\t($w, $x, $y, $z)\n";

    # step 7
    $w = shift @$input;
    my $w7 = $w;
    $x = $z % 26;                    # want x to be zero (again)
    $x = $x - 6;                     # want x to be zero (again)
    $z = int( $z / 26 );             # w2 + 14 - 6 = w7
    $x = int( $x != $w );            # w7 = w2 + 8
    $y = 25 * $x + 1;
    $z = $z * ( 25 * $x + 1 );
    $y = ( $w + 6 ) * $x;
    $z = $z + ( $w + 6 ) * $x;       # w1+6
    print "Testing: $z = ", $w1 + 6, "\n";
    print "Step  7\t($w, $x, $y, $z)\n";    # z = w1 + 6

    # step 8
    $w = shift @$input;
    my $w8 = $w;
    $x = 1;
    $y = $w + 3;
    $z = $z * 26 + $w + 3;                  # z = 26*(w1 + 6) + w8 + 3
    print "Testing: $z = ", 26 * ( $w1 + 6 ) + $w8 + 3, "\n";
    print "Step  8\t($w, $x, $y, $z)\n";

    # step 9
    $w = shift @$input;
    my $w9 = $w;
    print "z%26 = ", $z % 26, "\n";
    print "z%26 - 3 = ", $z % 26 - 3, "\n";
    $x = $z % 26 - 3;                       # x = w8 + 3 - 3 = w9
    $z = int( $z / 26 );                    # z = w1 + 6
    $x = int( $x != $w );
    $y = 25 * $x + 1;
    $z = $z * ( 25 * $x + 1 );
    $y = ( $w + 8 ) * $x;
    $z = $z + ( $w + 8 ) * $x;              # z = w1 + 6
    print "Testing: $z = ", $w1 + 6, "\n";
    print "Step  9\t($w, $x, $y, $z)\n";

    # step 10
    $w = shift @$input;
    my $w10 = $w;
    $x = 1;
    $y = $w + 14;
    $z = 26 * $z + $w + 14;                 # z = 26*(w1 + 6) + w10 + 14
    print "Testing: $z = ", 26 * ( $w1 + 6 ) + $w10 + 14, "\n";
    print "Step 10\t($w, $x, $y, $z)\n";

    # step 11
    $w = shift @$input;
    my $w11 = $w;
    $x = 1;
    $y = $w + 4;
    $z = 26 * $z + $w + 4;    # z = 26 * (26*(w1 + 6) + w10 + 14) + $w11 + 4
    print "Testing: $z = ", 26 * ( 26 * ( $w1 + 6 ) + $w10 + 14 ) + $w11 + 4,
      "\n";
    print "Step 11\t($w, $x, $y, $z)\n";

    # step 12
    $w = shift @$input;
    my $w12 = $w;
    $x = $z % 26 - 2;                        # x= w11 +4 - 2 = w12
    $x = int( $x != $w );                    # w12 = w11 + 2
    $z = int( $z / 26 ) * ( 25 * $x + 1 );
    $y = ( $w + 7 ) * $x;
    $z = $z + ( $w + 7 ) * $x;               # z = 26*(w1 + 6) + w10 + 14
    print "Testing: $z = ", 26 * ( $w1 + 6 ) + $w10 + 14, "\n";
    print "Step 12\t($w, $x, $y, $z)\n";

    # step 13                       (26^1)
    $w = shift @$input;
    my $w13 = $w;
    $x = $z % 26 - 9;                        # x = w10 + 14 - 9 = w13
    $z = int( $z / 26 );                     # w13 = w10 + 5
    $x = int( $x != $w );
    $z = $z * ( 25 * $x + 1 );
    $y = ( $w + 14 ) * $x;
    $z = $z + ( $w + 15 ) * $x;              # z = w1 + 6
    print "Step 13\t($w, $x, $y, $z)\n";
    print "Testing: $z = ", $w1 + 6, "\n";

    # step 14                       (26^0)
    $w = shift @$input;
    my $w14 = $w;
    $x = $z % 26 - 2;                              # x = w1 + 6
    $z = int( $z / 26 );                           # z = 0
    $x = int( $x != $w );                          # x = 0 => w1 + 6 - 2 = w14
    print "WTF: x = $x; w1 = $w1, w14 = $w14,  w1 + 6 = ",$w1 + 6,"\n";
    $y = ( $w + 1 ) * $x;                          # z = 0
    $z = $z * ( 25 * $x + 1 ) + ( $w + 1 ) * $x;
    print "Testing: $z = ", 0, "\n";
    print "Step 14\t($w, $x, $y, $z)\n";
    return ( $w, $x, $y, $z );
}

##############################################################################
package ALU;
##############################################################################
sub new {
    my $class = shift;
    my $self = bless {};
    $self->{-registers} = [ 0, 0, 0, 0 ];
    $self->set_input_stream( [] );
    return $self;
}

# ============================================================================
# parse the program and execute
# ============================================================================
sub debug {
    my $self = shift;
    $self->{-debug} = shift if @_;
    return $self->{-debug} || 0;
}

sub nowait {
    my $self = shift;
    $self->{-nowait} = shift if @_;
    return $self->{-nowait} || 0;
}

sub interpret {
    my $self         = shift;
    my $instructions = shift;

    my $pc = 0;
    $self->_set_reg( 'w', 0 );
    $self->_set_reg( 'x', 0 );
    $self->_set_reg( 'y', 0 );
    $self->_set_reg( 'z', 0 );

    foreach my $line (@$instructions) {

        $pc++;

        # 'real' instructions
        unless ( $line =~ /^break/ ) {
            my ( $instr, $a, $b ) =
              ( $line =~ /^(\w+)\s+([\w]+)\s+([-\w\d]+)?\s?#?/ );
            if ( defined $b ) {
                $b = $self->_get_reg($b) if $b =~ /^[A-Za-z]+$/;
            }
            $self->$instr( $a, $b );
        }

        # debug
        if ( $line =~ /^break/ || $self->debug ) {
            print "\nLine: \t$pc \t$line\n";
            foreach my $sym (qw(w x y z)) {
                print "$sym: ", $self->_get_reg($sym), "\n";
            }
            print "\nHit Enter to continue  ";
            <> unless $self->nowait;
        }
    }
    return (
             $self->_get_reg('w'), $self->_get_reg('x'),
             $self->_get_reg('y'), $self->_get_reg('z')
    );
}

# ============================================================================
# instructions
# ============================================================================
# inp a - Read an input value and write it to variable a.
sub inp {
    my $self   = shift;
    my $symbol = shift;
    my $value  = $self->_get_input();
    $self->_set_reg( $symbol, $value );
    return $self;
}

# add a b - Add the value of a to the value of b, then store the result in variable a
sub add {
    my $self = shift;
    my $a    = shift;
    my $b    = shift;
    $self->_set_reg( $a, $self->_get_reg($a) + $b );
    return $self;
}

# mul a b - Multiply the value of a by the value of b, then store the result in variable a.
sub mul {
    my $self = shift;
    my $a    = shift;
    my $b    = shift;
    $self->_set_reg( $a, $self->_get_reg($a) * $b );
    return $self;
}

# div a b - Divide the value of a by the value of b, truncate the
#           result to an integer, then store the result in variable a.
sub div {
    my $self = shift;
    my $a    = shift;
    my $b    = shift;
    die "dividing by zero\n" unless $b;
    $self->_set_reg( $a, int( $self->_get_reg($a) / $b ) );
    return $self;
}

# mod a b - Divide the value of a by the value of b, then store
#           the remainder in variable a.
sub mod {
    my $self = shift;
    my $a    = shift;
    my $b    = shift;
    die "modulus by zero\n" unless $b;
    $self->_set_reg( $a, $self->_get_reg($a) % $b );
    return $self;
}

# eql a b - If the value of a and b are equal, then store the
#           value 1 in variable a. Otherwise, store the value 0 in variable a.
sub eql {
    my $self = shift;
    my $a    = shift;
    my $b    = shift;
    $self->_set_reg( $a, int( $self->_get_reg($a) == $b ) );
    return $self;
}

# ============================================================================
# input stream
# ============================================================================
sub set_input_stream {
    my $self  = shift;
    my $input = shift;
    $self->{-input} = $input;
    return $self;
}

sub _get_input {
    my $self = shift;
    die("Ran out of input\n") unless scalar( @{ $self->{-input} } );
    return shift( @{ $self->{-input} } );
}

# ============================================================================
# registers
# ============================================================================
sub _reg {
    my $symbol = shift;
    return ord($symbol) - ord('w');
}

sub _set_reg {
    my $self   = shift;
    my $symbol = shift;
    my $value  = shift;
    $self->{-register}->[ _reg($symbol) ] = $value;
    return $self->{-register}->[ _reg($symbol) ];
}

sub _get_reg {
    my $self   = shift;
    my $symbol = shift;
    return $self->{-register}->[ _reg($symbol) ] || 0;
}

package main;
__DATA__
inp w
mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 6
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 14
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 15
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 1
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 6
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x 0
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -6
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 6
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 3
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -3
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 8
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 14
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 15
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 4
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -2
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 7
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -9
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 15
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -2
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 1
mul y x
add z y