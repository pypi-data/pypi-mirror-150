"""
    file under vectogebra - python module for vector algebra
    
    vectogrbra/__init__.py
    -------------------------
    This module contains the 'vector' class.
    -------------------------------------------------
    copyright: (C) 2022 Mohammad Maasir
    license: MIT License (see LICENSE in project's main directory)
    -------------------------------------------------
    date created: 9th of May, 2022 (3:09 AM)
    last modified: 9th of May, 2022
    -------------------------------------------------
    contributor(s): Mohammad Maasir
    -------------------------------------------------
    github: github.com/maasir554

"""



#importing vector class from vector.py

from src.vectogebra.vector import vector

"""
    to use vector object class, in your file, write: import vectogerbra.vector as v
    then you can use the vector class in your file
    example: v1 = v(1,2,3)

    to import the vector class in your file, you can use the following:
    ## import vectogerbra.vector as v [or any other alias name you want]
    ## from vectogerbra import vector as v [or any other alias name you want]
"""

#importing utility functions from utilities.py
import src.vectogebra.utilities 
