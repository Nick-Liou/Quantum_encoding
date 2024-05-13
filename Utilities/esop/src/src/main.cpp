
// Compile:
// g++ -std=c++17  main.cpp -o a  -fpermissive -Wint-to-pointer-cast -I ../easy/include  -I ../easy/lib/alice/include -I ../easy/lib/any -I ../easy/lib/bill/bill/include -I ../easy/lib/cli11 -I ../easy/lib/fmt -I ../easy/lib/json/include -I ../easy/lib/kitty/include -I ../easy/lib/lorina -I ../easy/lib/rang

//  -std=c++17 
// -fpermissive
// -Wint-to-pointer-cast


//  -I ../easy/lib/alice/include -I ../easy/lib/any -I ../easy/lib/bill/bill/include -I ../easy/lib/cli11 -I ../easy/lib/fmt -I ../easy/lib/json/include -I ../easy/lib/kitty/include -I ../easy/lib/lorina -I ../easy/lib/rang


// -I ../easy/include

// -I ../easy/lib/alice/include
// -I ../easy/lib/any               needed ??
// -I ../easy/lib/bill/bill/include
// -I ../easy/lib/cli11             needed ??
// -I ../easy/lib/fmt
// -I ../easy/lib/json/include
// -I ../easy/lib/kitty/include
// -I ../easy/lib/lorina
// -I ../easy/lib/rang



#include <easy/easy.hpp>
#include <easy/esop/esop_from_pkrm.hpp>
// #include <easy/esop/constructors.hpp>
// #include <easy/esop/exact_synthesis.hpp>
// #include <kitty/constructors.hpp>
// #include <kitty/print.hpp>

#include <iostream>
// #include <numeric>

#include <cstdlib> // for std::atoi

using namespace easy;

template<int NumVars>
inline kitty::static_truth_table<NumVars> from_hex( std::string const& hex )
{
  kitty::static_truth_table<NumVars> tt;
  kitty::create_from_hex_string( tt, hex );
  return tt;
}



/*! \brief Printer function for ESOP
 *
 * Print ESOP as an expression.
 *
 * \param esop ESOP
 * \param num_vars Number of variables
 * \param os Output stream
 */
inline void print_esop_as_exprs( const easy::esop::esop_t& esop, unsigned num_vars, std::ostream& os = std::cout )
{
  assert( num_vars <= 32 );
  os << esop.size() << ' ';
  for ( auto i = 0u; i < esop.size(); ++i )
  {
    const auto& c = esop[i];
    auto lit_count = c.num_literals();
    if ( lit_count == 0 )
    {
      os << "(1)";
    }
    else
    {
      os << "(";
      for ( auto j = 0u; j < num_vars; ++j )
      {
        if ( ( c._mask >> j ) & 1 )
        {
          os << ( ( ( c._bits >> j ) & 1 ) ? "x" : "~x" ) << j;
          --lit_count;
          if ( lit_count != 0 )
          {
            os << "*";
          }
        }
      }
      os << ")";
    }
    if ( i + 1 < esop.size() )
    {
      os << "^";
    }
  }
  // os << '\n';
}

int main(int argc, char* argv[]) {
   // Check if the correct number of command line arguments are provided
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <number_of_vars> <hex_string>" << std::endl;
        return 1;
    }



    // Extract number of variables from the command line argument
    const int number_of_vars = std::stoi(argv[1]);
    // Validate number_of_vars to be positive and within a reasonable range
    assert(number_of_vars > 0 && number_of_vars <= 32);
    
    // Extract hex string from the command line argument
    const std::string hex_string = argv[2];

    kitty::dynamic_truth_table tt(number_of_vars);
    kitty::create_from_hex_string(tt, hex_string);


    

    
    // std::cout << "Number of vars: "<< number_of_vars << " Hex string: " << hex_string << std::endl;



    // const unsigned number_of_vars = 3 ;
    // auto const tt = from_hex<number_of_vars>( "e8" );

    const auto cubes = esop::esop_from_optimum_pkrm( tt );


    // std::cout << std::endl << "His print" << std::endl;
    // easy::esop::print_esop_as_exprs(cubes,number_of_vars) ;
    
    // std::cout << std::endl << "My print" << std::endl;
    print_esop_as_exprs(cubes,number_of_vars) ;


    return 0;
}
