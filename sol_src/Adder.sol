// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.6.0;

contract adder
{
    
    ufixed     total;
    
    constructor() public
    {
        total =  100.0;
    }
    
    function add(ufixed a) public returns (ufixed)
    {
        total = total + a;
    }

    function mul(ufixed a) public returns (ufixed)
    {
        total = total * a;
    }



    function get_total() public view returns (ufixed)
    {
        return total;
    }
    
}

