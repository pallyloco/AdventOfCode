#!/usr/bin/perl
use strict;
use warnings;
open my $fh, "input_day16.txt" or die;
while ( my $code = <$fh> ) {
    chomp $code;
    next unless $code !~ /^\s*$/;
    $code =~ s/\s*$//;
    my $bits = Bstream->new($code);

    my $total = 0;
    $total = decode($bits);

    print "TOTAL: $total\n";
    print "Remaining bits: ", $bits->number_left, "\n";
}

sub decode {
    my $bits           = shift;
    my $state          = shift || State->new();
    
    my $added_versions = 0;
    my $version        = get_number( $bits, 3 );
    my $type           = get_number( $bits, 3 );

    my $depth = $state->depth;
    $state->remaining_bits( $state->remaining_bits - 6 );

    print " " x ( $depth * 2 ) . "VERSION: $version, TYPE: $type\n";

    # value
    if ( $type == 4 ) {
        decode_literal( $bits, $depth );
        return $version;
    }

    # operator
    else {
        
        # get the information about number of bits or number of records
        my $length_type = get_number( $bits, 1 );
        
        if ($length_type) {
            $state->remaining_operators( get_number( $bits, 11 ) );
        }
        else {
            $state->remaining_bits( get_number( $bits, 15 ) );
        }
        
        # setup a new state for the parameters
        my $new_state = State->new();
        $new_state->depth( $depth + 1 );

        # get the parameters
        while ( !$state->do_return ) {
            my $before = $bits->number_left;
            $added_versions += decode( $bits, $new_state );
            my $after = $bits->number_left;
            $state->remaining_bits( $state->remaining_bits - $before + $after );
            $state->remaining_operators( $state->remaining_operators - 1 );
        }
    }

    return $added_versions + $version;
}

sub get_number {
    my $bits           = shift;
    my $number_of_bits = shift || 0;
    my @bits           = $bits->next($number_of_bits);
    return BtoD->decimal( \@bits );
}

sub decode_literal {
    my $bits      = shift;
    my $depth     = shift;
    my $number    = 0;
    my $used_bits = 0;
    while ( $bits->not_empty ) {
        my $head_bit  = get_number( $bits, 1 );
        my $byte_bits = get_number( $bits, 4 );
        $number = $number * 16 + $byte_bits;
        $used_bits += 5;
        last unless $head_bit;
    }
    print " " x ( $depth * 2 ) . "Value: $number\n";
    return $used_bits;
}

# ==============================================================================
# state
# ==============================================================================
package State;

sub new {
    return
      bless { -depth => 0, -remaining_bits => 0, -remaining_operators => 0 };
}

sub do_return {
    my $self = shift;
#    return 1 if $self->{-depth} == 0;
    return 1
      if $self->{-remaining_bits} <= 0 && $self->{-remaining_operators} <= 0;
    return 0;
}

sub depth {
    my $self = shift;
    $self->{-depth} = shift if @_;
    return $self->{-depth};
}

sub remaining_bits {
    my $self = shift;
    $self->{-remaining_bits} = shift if @_;
    return $self->{-remaining_bits};
}

sub remaining_operators {
    my $self = shift;
    $self->{-remaining_operators} = shift if @_;
    return $self->{-remaining_operators};
}

# ==============================================================================
# binary to decimal
# ==============================================================================
package BtoD;

sub decimal {
    my $class  = shift;
    my $bits   = shift;
    my $number = 0;
    while (@$bits) {
        my $bit = shift @$bits;
        $number = $number * 2 + $bit;
    }
    return $number;
}

# ==============================================================================
# Byte Stream
# ==============================================================================
package Bstream;

sub new {
    my $class      = shift;
    my $hex_string = shift;
    my $self       = { -hex => [ split "", $hex_string ], -binary => [] };
    return bless $self;
}

sub next {
    my $self     = shift;
    my $how_many = shift || 1;
    my $binary   = $self->_binary;
    my @next;
    foreach my $i ( 1 .. $how_many ) {
        if ( $self->not_empty ) {
            my $next = $self->_next_binary;
            push @next, $next if defined $next;
        }
    }
    return @next;
}

sub not_empty {
    my $self   = shift;
    my $hex    = $self->_hex;
    my $binary = $self->_binary;
    return ( scalar(@$binary) + 4 * scalar(@$hex) );
}

sub number_left {
    my $self = shift;
    return $self->not_empty;
}

sub _next_binary {
    my $self   = shift;
    my $binary = $self->_binary;
    unless ( $self->_size_of_binary ) {
        my $str = $self->_next_hex;
        $self->_add_hex_to_binary($str);
    }
    return shift(@$binary) if $self->_size_of_binary;
    return;
}

sub _add_hex_to_binary {
    my $self = shift;
    my $hex  = shift;
    return unless defined $hex;
    if    ( $hex eq "0" ) { $self->_add_to_binary( split "", "0000" ); }
    elsif ( $hex eq "1" ) { $self->_add_to_binary( split "", "0001" ); }
    elsif ( $hex eq "2" ) { $self->_add_to_binary( split "", "0010" ); }
    elsif ( $hex eq "3" ) { $self->_add_to_binary( split "", "0011" ); }
    elsif ( $hex eq "4" ) { $self->_add_to_binary( split "", "0100" ); }
    elsif ( $hex eq "5" ) { $self->_add_to_binary( split "", "0101" ); }
    elsif ( $hex eq "6" ) { $self->_add_to_binary( split "", "0110" ); }
    elsif ( $hex eq "7" ) { $self->_add_to_binary( split "", "0111" ); }
    elsif ( $hex eq "8" ) { $self->_add_to_binary( split "", "1000" ); }
    elsif ( $hex eq "9" ) { $self->_add_to_binary( split "", "1001" ); }
    elsif ( $hex eq "A" ) { $self->_add_to_binary( split "", "1010" ); }
    elsif ( $hex eq "B" ) { $self->_add_to_binary( split "", "1011" ); }
    elsif ( $hex eq "C" ) { $self->_add_to_binary( split "", "1100" ); }
    elsif ( $hex eq "D" ) { $self->_add_to_binary( split "", "1101" ); }
    elsif ( $hex eq "E" ) { $self->_add_to_binary( split "", "1110" ); }
    elsif ( $hex eq "F" ) { $self->_add_to_binary( split "", "1111" ); }
}

sub _add_to_binary {
    my $self   = shift;
    my $binary = $self->_binary;
    push @$binary, @_;
}

sub _hex {
    my $self = shift;
    $self->{-hex};
}

sub _next_hex {
    my $self = shift;
    my $hex  = $self->_hex;
    if ( $self->_hex_is_not_empty ) {
        return shift(@$hex);
    }
    return;
}

sub _hex_is_not_empty {
    my $self = shift;
    my $hex  = $self->_hex;
    return scalar(@$hex);
}

sub _binary {
    my $self = shift;
    return $self->{-binary};
}

sub _size_of_binary {
    my $self = shift;
    $self = scalar( @{ $self->_binary } );
}

# ==============================================================================
# DATA
# ==============================================================================
package main;

__DATA__
A0016C880162017C3686B18A3D4780                 
                      
                      





