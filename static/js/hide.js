function cacher(coll)
{
	var elmt = document.getElementById('dataTable');
	var elmtsCellule = 'th|td'.split('|');
	for(j=0; j < elmtsCellule.length; j++)
	{
		var cells = elmt.getElementsByTagName(elmtsCellule[ j]);
		for (i=0; i < cells.length; i++)
			if (cells[ i ].className == coll)
				if (cells[ i ].style.display != 'none')
					cells[ i ].style.display = 'none';
				else
					try
						{cells[ i ].style.display = 'table-cell';}
					catch (ex)
						{cells[ i ].style.display = 'block';}
	}
}



function cacher(coll)
{
	var elmt = document.getElementById('dataTable_1');
	var elmtsCellule = 'th|td'.split('|');
	for(j=0; j < elmtsCellule.length; j++)
	{
		var cells = elmt.getElementsByTagName(elmtsCellule[ j]);
		for (i=0; i < cells.length; i++)
			if (cells[ i ].className == coll)
				if (cells[ i ].style.display != 'none')
					cells[ i ].style.display = 'none';
				else
					try
						{cells[ i ].style.display = 'table-cell';}
					catch (ex)
						{cells[ i ].style.display = 'block';}
	}
}
