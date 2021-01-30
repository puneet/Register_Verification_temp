/*
 * Range lookup functions
 *
 * Authors:
 *   Michael Meeks <michael@ximian.com>
 *   Jukka-Pekka Iivonen <iivonen@iki.fi>
 *   JP Rosevear <jpr@arcavia.com>
 *   Morten Welinder (terra@gnome.org)
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, see <https://www.gnu.org/licenses/>.
 */

#include <gnumeric-config.h>
#include <gnumeric.h>
#include <func.h>

#include <parse-util.h>
#include <dependent.h>
#include <cell.h>
#include <collect.h>
#include <sheet.h>
#include <value.h>
#include <ranges.h>
#include <expr.h>
#include <expr-impl.h>
#include <application.h>
#include <expr-name.h>
#include <mathfunc.h>
#include <gutils.h>
#include <workbook.h>
#include <sheet.h>
#include <parse-util.h>
#include <gnm-i18n.h>

#include <goffice/goffice.h>
#include <gnm-plugin.h>

#include <string.h>
#include <stdlib.h>

GNM_PLUGIN_MODULE_HEADER;

/* -------------------------------------------------------------------------- */
/***************************************************************************/

static GnmFuncHelp const help_columnnum[] = {
	{ GNM_FUNC_HELP_NAME, F_("COLUMN:vector of column numbers") },
	{ GNM_FUNC_HELP_ARG, F_("x:reference, defaults to the position of the current expression") },
	{ GNM_FUNC_HELP_DESCRIPTION, F_("COLUMN function returns a Nx1 array containing the sequence "
					"of integers "
					"from the first column to the last column of @{x}.") },
	{ GNM_FUNC_HELP_NOTE, F_("If @{x} is neither an array nor a reference nor a range, "
				 "returns #VALUE!") },
	{ GNM_FUNC_HELP_EXAMPLES, "=COLUMN(A1:C4)" },
	{ GNM_FUNC_HELP_EXAMPLES, "=COLUMN(A:C)" },
	{ GNM_FUNC_HELP_EXAMPLES, F_("column() in G13 equals 7.") },
	{ GNM_FUNC_HELP_SEEALSO, "COLUMNS,ROW,ROWS" },
	{ GNM_FUNC_HELP_END }
};

static GnmValue *
gnumeric_columnnum (GnmFuncEvalInfo *ei, GnmValue const * const *args)
{
	int col, width, i;
	GnmValue *res;
	GnmValue const *ref = args[0];

	if (ref == NULL) {
		col   = ei->pos->eval.col + 1; /* user visible counts from 0 */
		if (eval_pos_is_array_context (ei->pos))
			gnm_expr_top_get_array_size (ei->pos->array_texpr, &width, NULL);
		else
			return value_new_int (col);
	} else if (VALUE_IS_CELLRANGE (ref)) {
		Sheet    *tmp;
		GnmRange  r;

		gnm_rangeref_normalize (&ref->v_range.cell, ei->pos, &tmp, &tmp, &r);
		col    = r.start.col + 1;
		width  = range_width (&r);
	} else
		return value_new_error_VALUE (ei->pos);

	if (width == 1)
		return value_new_int (col);

	res = value_new_array (width, 1);
	for (i = width; i-- > 0 ; )
		value_array_set (res, i, 0, value_new_int (col + i));
	return res;
}

/***************************************************************************/

/***************************************************************************/

static GnmFuncHelp const help_rownum[] = {
	{ GNM_FUNC_HELP_NAME, F_("ROW:vector of row numbers") },
	{ GNM_FUNC_HELP_ARG, F_("x:reference, defaults to the position of the current expression") },
	{ GNM_FUNC_HELP_DESCRIPTION, F_("ROW function returns a 1xN array containing the "
					"sequence of integers "
					"from the first row to the last row of @{x}.") },
	{ GNM_FUNC_HELP_NOTE, F_("If @{x} is neither an array nor a reference nor a range, "
				 "returns #VALUE!") },
	{ GNM_FUNC_HELP_EXAMPLES, "=ROW(A1:D3)" },
	{ GNM_FUNC_HELP_EXAMPLES, "=ROW(1:3)" },
	{ GNM_FUNC_HELP_SEEALSO, "COLUMN,COLUMNS,ROWS" },
	{ GNM_FUNC_HELP_END }
};

static GnmValue *
gnumeric_rownum (GnmFuncEvalInfo *ei, GnmValue const * const *args)
{
	int row, n, i;
	GnmValue *res;
	GnmValue const *ref = args[0];

	if (ref == NULL) {
		row   = ei->pos->eval.row + 1; /* user visible counts from 0 */
		if (eval_pos_is_array_context (ei->pos))
			gnm_expr_top_get_array_size (ei->pos->array_texpr, NULL, &n);
		else
			return value_new_int (row);
	} else if (VALUE_IS_CELLRANGE (ref)) {
		Sheet    *tmp;
		GnmRange  r;

		gnm_rangeref_normalize (&ref->v_range.cell, ei->pos, &tmp, &tmp, &r);
		row    = r.start.row + 1;
		n = range_height (&r);
	} else
		return value_new_error_VALUE (ei->pos);

	if (n == 1)
		return value_new_int (row);

	res = value_new_array (1, n);
	for (i = n ; i-- > 0 ; )
		value_array_set (res, 0, i, value_new_int (row + i));
	return res;
}

/***************************************************************************/

/***************************************************************************/

GnmFuncDescriptor const lookup_functions[] = {
	{ "columnnum",     "|A",
	  help_column,   gnumeric_column, NULL,
	  GNM_FUNC_SIMPLE, GNM_FUNC_IMPL_STATUS_COMPLETE, GNM_FUNC_TEST_STATUS_BASIC },
	{ "rownum",       "|A",
	  help_row,      gnumeric_row, NULL,
	  GNM_FUNC_SIMPLE, GNM_FUNC_IMPL_STATUS_COMPLETE, GNM_FUNC_TEST_STATUS_BASIC },
        {NULL}
};

G_MODULE_EXPORT void
go_plugin_init (GOPlugin *plugin, GOCmdContext *cc)
{
	debug_lookup_caches = gnm_debug_flag ("lookup-caches");
	g_signal_connect (gnm_app_get_app (), "recalc-clear-caches",
			  G_CALLBACK (clear_caches), NULL);
}

G_MODULE_EXPORT void
go_plugin_shutdown (GOPlugin *plugin, GOCmdContext *cc)
{
	g_signal_handlers_disconnect_by_func (gnm_app_get_app (),
					      G_CALLBACK (clear_caches), NULL);

	if (protect_string_pool) {
		g_printerr ("Imbalance in string pool: %d\n", (int)protect_string_pool);
		protect_string_pool = 0;
	}
	if (protect_float_pool) {
		g_printerr ("Imbalance in float pool: %d\n", (int)protect_float_pool);
		protect_float_pool = 0;
	}

	clear_caches ();
}
