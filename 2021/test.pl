#!/usr/bin/perl
use strict;
use warnings;
hello->new();
foo();
sub foo {
    print "hello\n";
    my $x = sub {
        print "This is an internal sub\n";
        return;
    };
    $x->();
    print "goodbye\n";
}

my $x = Spot->new(1,3);
my $y = Spot->new(2,4);
my $z = $x + $y;

package hello;
use overload "+"=>'add';

    my $str =  "in package\n";
    sub new {
        
        print $str;
        return bless {-boo=>1};
    }
sub add {
    use Data::Dumper;print Dumper \@_;
}


package Spot;
use strict;
use warnings;

use overload "==" => "equals", '""' => "stringification", "+"=>'plus';

sub new {
    my $class = shift;
    my $row   = shift || 0;
    my $col   = shift || 0;
    my $self  = bless {};
    $self->row($row);
    $self->col($col);
    return $self;
}

sub is_circular {
    my $self = shift;
    $self->{-circular} = shift if @_;
}

sub max_row {
    my $self = shift;
    $self->{-max_row} = shift if @_;
    return $self->{-max_row} || 10;
}

sub max_col {
    my $self = shift;
    $self->{-max_col} = shift if @_;
    return $self->{-max_col} || 10;
}


sub row {
    my $self = shift;
    $self->{-row} = shift if @_;
    return $self->{-row};
}

sub col {
    my $self = shift;
    $self->{-col} = shift if @_;
    return $self->{-col};
}

sub plus {
    print join ", ",caller,"\n";
    use Data::Dumper; print "plus:\n",Dumper \@_;die;
    my $self = shift;
    my $other = shift;
    my $row = $self->row + $other->row;
    my $col = $self->col + $other->col;
    if ($self->circular) {
        my $max_row = $self->max_row;
        my $max_col = $self->max_col;
        $row = $row%$max_row;
        $col = $col%$max_row;
    }
    return Spot->new($row,$col);
    return 
}
sub down {
    my $self = shift;
    return Spot->new( $self->row + 1, $self->col );
}

sub up {
    my $self = shift;
    return Spot->new( $self->row - 1, $self->col );
}

sub right {
    my $self = shift;
    return Spot->new( $self->row, $self->col + 1 );
}

sub left {
    my $self = shift;
    return Spot->new( $self->row, $self->col - 1 );
}

sub equals {
    my $self  = shift;
    my $other = shift;
    return $self->row == $other->row && $self->col == $other->col;
}

sub stringification {
    my $self = shift;
    return "[" . $self->row . "," . $self->col . "]";
}

