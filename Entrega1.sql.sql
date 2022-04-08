
CREATE TABLE Exportaciones(
	SUBPARTIDA varchar(150) NOT NULL
	DESCRIPCIÓN ARANCELARIA	str NOT NULL
	DISTRITO str NOT NULL CHECK( DISTRITO = “Guayaquil” or “Quito” or “Manta” or “Esmeraldas” or “Puerto Bolivar” or “ Cuenca”)
	PAIS_DESTINO str NOT NULL
	TIPO_UNIDAD_FISICA Str NOT NULL  CHECK( TIPO UNIDAD= “unidades” or “kilogramo” or “pares” or “millar” or “litro” or “quilate”  or “metro”)
	CANTIDAD_UNIDAD_F__SICA	varchar(150) NOT NULL 
	PESO_NETO_KG	varchar(150) NOT NULL
	FOB_DOLARES	varchar(150) NOT NULL 
	FOREIGN KEY (PAIS_DESTINO) REFERENCES Ingresos en miles de dolares por importaciones(Importadores)
);
CREATE TABLE Importaciones(
	SUBPARTIDA varchar(150) NOT NULL
	DESCRIPCI__N_ARANCELARIA	str NOT NULL
	DISTRITO str NOT NULL CHECK( DISTRITO = “Guayaquil” or “Quito” or “Manta” or “Esmeraldas” or “Puerto Bolívar” or “ Cuenca”)
	PA__S_ORIGEN str NOT NULL
	TIPO_UNIDAD_F__SICA	str NOT NULL
	TIPO_UNIDAD_FISICA Str NOT NULL  CHECK( TIPO UNIDAD= “unidades” or “kilogramo” or “pares” or “millar” or “litro” or “quilate”  or “metro”)
	PESO_NETO__KG	varchar(150) NOT NULL
	CIF__D__LARES	varchar(150) NOT NULL 
	FOREIGN KEY (PA__S_ORIGEN) REFERENCES Ingresos en miles de dólares por importaciones(Importadores)
);
CREATE TABLE Ingresos en miles de dolares por importaciones(
	Importadores	str NOT NULL	
	Valor_exportado_en_2016	int
	Valor_exportado_en_2017	int
	Valor_exportado_en_2018	int
	Valor_exportado_en_2019	int
	Valor_exportado_en_2020	int
	PRIMARY KEY(Importadores)
);
CREATE TABLE `proyecto-analitica-de-negocios.Datawarehouse.compras_pais` AS
		SELECT P__S_ORIGEN, SUM(CIF__D__LARES_) AS sum_compras FROM `proyecto-analitica-de-negocios.Datawarehouse.Importaciones` GROUP BY P__S_ORIGEN 
	CREATE TABLE `proyecto-analitica-de-negocios.Datawarehouse.Ingresos_pais` AS
		SELECT PAIS_DESTINO, SUM(FOB_DOLARES) AS sumdolares FROM `proyecto-analitica-de-negocios.Datawarehouse.Exportaciones` GROUP BY PAIS_DESTINO 
SELECT PAIS_DESTINO,(Ingresos.sumdolares+Compras.sum_compras) AS totalcomercial 
FROM `proyecto-analitica-de-negocios.Datawarehouse.Ingresos_pais` Ingresos
INNER JOIN `proyecto-analitica-de-negocios.Datawarehouse.compras_pais` Compras
ON (
Ingresos.PAIS_DESTINO = Compras.PA__S_ORIGEN
)
ORDER BY totalcomercial DESC;
SELECT PAIS_DESTINO FROM `proyecto-analitica-de-negocios.Datawarehouse.Exportaciones` ORDER BY FOB_DOLARES DESC;
SELECT PAIS_DESTINO, AVG(FOB_DOLARES) AS avg_exp FROM `proyecto-analitica-de-negocios.Datawarehouse.Exportaciones` WHERE PAIS_DESTINO IN ('CO-COLOMBIA', 'PE-PERU') GROUP BY PAIS_DESTINO ;
SELECT PA__S_ORIGEN,(Ing.sumdolares-Comp.sum_compras) AS difcomercial 
FROM `proyecto-analitica-de-negocios.Datawarehouse.Ingresos_pais` Ing
		INNER JOIN `proyecto-analitica-de-negocios.Datawarehouse.compras_pais` Comp
    ON Ing.PAIS_DESTINO=Comp.PA__S_ORIGEN 
  WHERE PA__S_ORIGEN  LIKE 'US-ESTADOS UNIDOS';
SELECT DISTRITO, SUM(FOB_DOLARES) AS sum_exp FROM `proyecto-analitica-de-negocios.Datawarehouse.Exportaciones` GROUP BY DISTRITO ORDER BY sum_exp DESC;
SELECT LTRIM(DESCRIPCION_ARANCELARIA) AS PRODUCTOS FROM `proyecto-analitica-de-negocios.Datawarehouse.Exportaciones`;
SELECT DESCRIPCION_ARANCELARIA, SUM(CANTIDAD_UNIDAD_F__SICA) AS VALOR_COMERCIAL FROM `proyecto-analitica-de-negocios.Datawarehouse.Exportaciones` 
	GROUP BY DESCRIPCION_ARANCELARIA 
	ORDER BY VALOR_COMERCIAL DESC; 
SELECT SUM(CIF__D__LARES_) AS COSTO_PRODUCTO, SUM(CANTIDAD_F__SICA) AS CANTIDAD,DESCRIPCI__N_ARANCELARIA  FROM `proyecto-analitica-de-negocios.Datawarehouse.Importaciones` 
	WHERE CANTIDAD_F__SICA >= 1 
	GROUP BY DESCRIPCI__N_ARANCELARIA  
	ORDER BY (COSTO_PRODUCTO/CANTIDAD) DESC;
SELECT SUM(FOB_DOLARES) AS INGRESOS, DESCRIPCION_ARANCELARIA, SUM(CANTIDAD_UNIDAD_F__SICA) AS CANTIDAD FROM `proyecto-analitica-de-negocios.Datawarehouse.Exportaciones` WHERE CANTIDAD_UNIDAD_F__SICA >= 1  
	GROUP BY DESCRIPCION_ARANCELARIA
	ORDER BY INGRESOS/CANTIDAD DESC;
SELECT DESCRIPCI__N_ARANCELARIA, SUM(CANTIDAD_F__SICA) AS CANTIDAD FROM `proyecto-analitica-de-negocios.Datawarehouse.Importaciones` GROUP BY DESCRIPCI__N_ARANCELARIA ORDER BY CANTIDAD ASC LIMIT 8
SELECT SUM(CANTIDAD_UNIDAD_F__SICA) AS CANTIDAD, DESCRIPCION_ARANCELARIA FROM `proyecto-analitica-de-negocios.Datawarehouse.Exportaciones` GROUP BY DESCRIPCION_ARANCELARIA ORDER BY CANTIDAD ASC LIMIT 8
SELECT Importadores,Valor_exportado_en_2016 FROM `proyecto-analitica-de-negocios.Datawarehouse.Ingresos en miles de dólares por importaciones` 
	where Valor_exportado_en_2016<16797667
	order by Valor_exportado_en_2016 desc  
	limit 3;
SELECT Importadores,Valor_exportado_en_2018 FROM `proyecto-analitica-de-negocios.Datawarehouse.Ingresos en miles de dolares por importaciones` 
	where Valor_exportado_en_2018<21627978
	order by Valor_exportado_en_2018 desc  
	limit 3;
SELECT Importadores,Valor_exportado_en_2020 FROM `proyecto-analitica-de-negocios.Datawarehouse.Ingresos en miles de dolares por importaciones` 
	where Valor_exportado_en_2020<20226568
	order by Valor_exportado_en_2020 desc  
	limit 3;
SELECT *, (Valor_exportado_en_2016+Valor_exportado_en_2017+Valor_exportado_en_2018+Valor_exportado_en_2019+Valor_exportado_en_2020) AS Total FROM `proyecto-analitica-de-negocios.Datawarehouse.Ingresos en miles de dolares por importaciones`
	where (Valor_exportado_en_2016+Valor_exportado_en_2017+Valor_exportado_en_2018+Valor_exportado_en_2019+Valor_exportado_en_2020)<100073944
	ORDER BY Total desc
	limit 5;
SELECT LOWER(PAIS_DESTINO) AS PAIS,COUNT(PAIS_DESTINO) AS TOTAL_PEDIDOS_ARANCELARIOS,SUM(FOB_DOLARES)AS VALOR_TOTAL FROM `proyecto-analitica-de-negocios.Datawarehouse.Exportaciones`
	group by PAIS
	order by COUNT(PAIS) desc
	limit 3;
SELECT Exp.PAIS_DESTINO
	FROM `proyecto-analitica-de-negocios.Datawarehouse.Exportaciones` Exp
	INNER JOIN `proyecto-analitica-de-negocios.Datawarehouse.SUMYPROMDOL` syp
	on (
		Exp.PAIS_DESTINO=syp.PAIS_DESTINO
		)
	WHERE syp.TOTAL_VALOR_ARANCELARIO > 229771.5
	GROUP BY PAIS_DESTINO;
select DISTRITO , CAST(SUM( CANTIDAD_UNIDAD_F__SICA) as numeric) as CANTIDADES_TOTALES from `proyecto-analitica-de-negocios.Datawarehouse.Exportaciones` 
	group by DISTRITO 
	order by CANTIDADES_TOTALES desc
	limit 3;







