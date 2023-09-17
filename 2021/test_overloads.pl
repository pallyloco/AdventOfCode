#!/usr/bin/perl
use strict;
use warnings;

print Foo->new( 1, 2 ), "==", Foo->new( 3, 4 ), " ? ",
  Foo->new( 1, 2 ) == Foo->new( 3, 4 ), "\n";
print Foo->new( 1, 2 ), "==", Foo->new( 1, 3 ), " ? ",
  Foo->new( 1, 2 ) == Foo->new( 1, 3 ), "\n";
print Foo->new( 1, 2 ), "==", Foo->new( 3, 2 ), " ? ",
  Foo->new( 1, 2 ) == Foo->new( 3, 2 ), "\n";
print Foo->new( 1, 2 ), "==", Foo->new( 1, 2 ), " ? ",
  Foo->new( 1, 2 ) == Foo->new( 1, 2 ), "\n";

package Foo;
use overload "==" => "equals", '""' => "stringification";

sub new {
    my $class = shift;
    my $row   = shift;
    my $col   = shift;
    return bless { -row => $row, -col => $col };
}

sub equals {
    my $self  = shift;
    my $other = shift;
    return $self->{-row} == $other->{-row} && $self->{-col} == $other->{-col};
}

sub stringification {
    my $self = shift;
    return "[" . $self->{-row} . "," . $self->{-col} . "]";
}
