dnl Process this file with autoconf to produce a configure script.

AC_PREREQ([2.69])
# change version number here and below in LIB_*
AC_INIT([librabinpoly], [0.11.0])
AC_CONFIG_SRCDIR([src/rabinpoly.c])
AC_CONFIG_HEADER([config.h])

# http://www.freesoftwaremagazine.com/articles/building_shared_libraries_once_using_autotools
LIB_CURRENT=0
LIB_REVISION=11
LIB_AGE=0
AC_SUBST(LIB_CURRENT)
AC_SUBST(LIB_REVISION)
AC_SUBST(LIB_AGE)

AC_SUBST(VERSION)

# Checks for programs.
AC_PROG_CXX
AC_PROG_AWK
AC_PROG_CC
AC_PROG_CPP
AC_PROG_INSTALL
AC_PROG_LN_S
AC_PROG_MAKE_SET
AC_PROG_MKDIR_P

LT_INIT

# Checks for header files.
AC_CHECK_HEADERS([stdlib.h string.h openssl/md5.h])
AC_SEARCH_LIBS([MD5_Update], [crypto])


# Checks for typedefs, structures, and compiler characteristics.
AC_C_INLINE

# Checks for library functions.
AC_FUNC_MALLOC
AC_CHECK_FUNCS([bzero])

AC_CONFIG_FILES([Makefile
                 python/Makefile
                 src/Makefile
                 test/Makefile])

AC_MSG_CHECKING(whether compiler understands -Wall)
old_CFLAGS="$CFLAGS"
CFLAGS="$CFLAGS -Wall"
AC_TRY_COMPILE([],[],
               AC_MSG_RESULT(yes),
               AC_MSG_RESULT(no)
               CFLAGS="$old_CFLAGS")

AM_INIT_AUTOMAKE

AC_OUTPUT

