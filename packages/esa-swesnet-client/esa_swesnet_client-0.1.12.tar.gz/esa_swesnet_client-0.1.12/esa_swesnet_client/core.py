
#####################################################################
#                     ___ _ __   __ _ _ __ ___                      #
#                    / __| '_ \ / _` | '__/ __|                     #
#                    \__ | |_) | (_| | | | (__                      #
#                    |___| .__/ \__,_|_|  \___|                     #
#                        |_|                                        #
#                                                                   #
# The IPR of this software belongs to Space Applications & Research #
# Consultancy (SPARC). The usage is at the discretion of SPARC and  #
# licenses for its use should be addressed to the Contracts Dept.   #
# at SPARC:                                                         #
#                                                                   #
#   Space Applications & Research Consultancy (SPARC)               #
#   68 Aiolou Street                                                #
#   Athens 10551                                                    #
#   Greece                                                          #
#                                                                   #
# For technical issues contact:                                     #
#                                                                   #
# Dr. Ingmar Sandberg: sandberg@sparc.gr                            #
#                                                                   #
# ©2023 SPARC                                                       #
#                                                                   #
#####################################################################

from . import *

import requests
import json

####################################################################

def get_cookies( username , password ) :

    try :

        response = requests.post( 
            "https://sso.ssa.esa.int/am/json/authenticate" ,
            headers = {
                "Content-Type" : "application/json" ,
                "X-OpenAM-Username" : username ,
                "X-OpenAM-Password" : password ,
            } ,
            data = "{}"
        )

        token_dict = json.loads( response.content )

        #print(response.text)

        return( get_session_cookies( token_dict[ "tokenId" ] ) )

    except Exception as exc :
        print( exc )

    return( False , "" )

def get_session_cookies( auth_cookie ) :

    try :
        init_response = requests.get(
            "https://swe.ssa.esa.int/hapi/capabilities" ,
            cookies = {
                "iPlanetDirectoryPro" : auth_cookie ,
            }
        )

        cookie_jar = init_response.history[ 0 ].cookies
        jsession_id = cookie_jar.get( "JSESSIONID" )
        xsrf_token = cookie_jar.get( "XSRF-TOKEN" )
        consent_url = init_response.url
        content = init_response.content

        if not "/hapi/capabilities" in consent_url :

            consent_response = requests.post(
                consent_url ,
                cookies = {
                    "iPlanetDirectoryPro" : auth_cookie ,
                    "JSESSIONID" : jsession_id ,
                    "XSRF_TOKEN" : xsrf_token ,
                },
                data = {
                    "decision" : "Allow" ,
                    "save_consent" : "on" ,
                }
            )

            content = consent_response.content
            
        capabilities = json.loads( content )
        #print(capabilities)
        #version = capabilities[ "version" ]
        status = capabilities[ "status" ]
        if status != { } and status[ "message" ] == "OK" :
            return( { "JSESSIONID" : jsession_id , "XSRF_TOKEN" : xsrf_token } )
    except Exception as exc :
        print( exc )

    return( False )

####################################################################

def get_data( url , cookies ) :

    #print(url)

    response = requests.get(
        url ,
        cookies = cookies
    )
    
    data = json.loads( response.content )
    
    return( data )

####################################################################

def fetch( username=False , password=False , url=False ) :
    if not username or not password or not url : return( False )

    cookies = get_cookies( username , password )

    if not ( type( cookies ) is dict ) : return( False )
    if not ( "JSESSIONID" in cookies ) : return( False )
    if not ( "XSRF_TOKEN" in cookies ) : return( False )

    res = get_data( url , cookies )

    return( res )

