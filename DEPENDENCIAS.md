# Dependencias — Factura Electrónica El Salvador (DTE)

Guía de qué necesita tener instalado el cliente para que la solución funcione
correctamente, separando lo que **viene con Odoo** de lo que **se entrega en
este repositorio**.

> Compatible con **Odoo 19.0**. La facturación electrónica (DTE) funciona en
> **Odoo Community**. Solo las áreas de **RRHH/Planilla** y **Despacho** requieren
> **Odoo Enterprise** (ver sección 3).

---

## 1. Apps de Odoo que el cliente debe activar (incluidas en Odoo)

No se entregan en este repo; el cliente las activa desde **Aplicaciones**. Todas
están disponibles en **Odoo Community**.

| Módulo Odoo | Para qué sirve |
|---|---|
| `account` | Contabilidad / Facturación |
| `sale` / `sale_management` | Ventas |
| `purchase` | Compras |
| `stock` | Inventario |
| `contacts` | Contactos |
| `product`, `uom` | Productos y unidades de medida |
| `phone_validation` | Validación de teléfonos *(requiere la librería Python `phonenumbers`)* |
| `l10n_latam_base` | Base de localización LATAM |
| `l10n_latam_invoice_document` | Tipos de documento LATAM |
| `account_debit_note` | Notas de débito |
| `hr`, `hr_attendance`, `resource` | RRHH base |
| `fleet`, `mail`, `web` | Flota, correo, framework web |

## 2. Librerías de Python requeridas

| Librería | La usa |
|---|---|
| `phonenumbers` | `phone_validation` (validación de teléfonos) |
| `requests` | `shopify_fast_connector` (y los servicios web de Hacienda) |

Instalación típica:

```bash
pip install phonenumbers requests
```

## 3. ⚠️ Apps de Odoo Enterprise (de pago — NO están en Community)

Estos módulos **no existen en Odoo Community**. Si el cliente está en Community,
las áreas que dependen de ellos **no se podrán instalar**.

| App Enterprise | La exige | Área afectada |
|---|---|---|
| **`hr_payroll`** (Nómina) | `hr_retenciones_sv_dte`, `hr_asignaciones_sv_dte`, `planilla_unica_sv_dte`, `rrhh_base_sv_dte` | RRHH / Planilla |
| **`stock_barcode`** (Código de barras) | `despacho_sv_dte` | Despacho |

> ✅ Toda la **facturación electrónica (DTE)** funciona en **Odoo Community**.
> ⚠️ **RRHH/Planilla** y **Despacho** requieren **Odoo Enterprise**.

---

## 4. Módulos de este repositorio (los que se entregan al cliente)

### 4.1 Cadena de Facturación Electrónica (DTE)

Orden de instalación (cada módulo arrastra a sus dependencias):

```
base_sv_dte
  └─ sv_dte
       └─ invoice_sv_dte
            └─ hacienda_sv_dte
                 └─ haciendaws_fe_sv_dte   (núcleo de envío a Hacienda)
                      ├─ hacienda_contingencia_sv_dte
                      ├─ hacienda_fex_sv_dte           (exportación)
                      ├─ hacienda_fse_sv_dte           (sujeto excluido)
                      ├─ hacienda_invalidadion_sv_dte  (invalidaciones)
                      └─ mh_anexos_sv_dte              (anexos MH)
```

Módulos de apoyo (se instalan según se necesiten):
`common_utils_sv_dte`, `journal_sequence_sv_dte`, `quedan_sv_dte`,
`partidas_sv_dte`, `reportes_ventas_sv_dte`, `purchase_sv_dte`,
`hacienda_payment_terms_sv_dte`, `dte_import_sv_dte`, `dpto_sv_dte`.

### 4.2 RRHH / Planilla (requiere Enterprise: `hr_payroll`)

```
hr_retenciones_sv_dte
  ├─ rrhh_base_sv_dte
  ├─ hr_asignaciones_sv_dte
  └─ planilla_unica_sv_dte
```

### 4.3 Despacho (requiere Enterprise: `stock_barcode`)

```
despacho_sv_dte   (depende de dpto_sv_dte, hacienda_sv_dte, stock, stock_barcode, sale, fleet, hr...)
```

### 4.4 Integraciones

```
shopify_fast_connector   (sale_management, account, stock, product, contacts, mail + requests)
```

---

## 5. Tabla completa: dependencias por módulo del repo

| Módulo (este repo) | Depende de |
|---|---|
| `base_sv_dte` | base |
| `common_utils_sv_dte` | — |
| `dpto_sv_dte` | — |
| `sv_dte` | base, base_sv_dte, account, phone_validation, l10n_latam_base |
| `invoice_sv_dte` | base, sv_dte, account, product, mail |
| `hacienda_sv_dte` | base_sv_dte, sv_dte, contacts, account |
| `haciendaws_fe_sv_dte` | hacienda_sv_dte, base_sv_dte, invoice_sv_dte, account_debit_note, l10n_latam_invoice_document, common_utils_sv_dte |
| `hacienda_contingencia_sv_dte` | base, sv_dte, account, hacienda_sv_dte, base_sv_dte, haciendaws_fe_sv_dte |
| `hacienda_fex_sv_dte` | base, hacienda_sv_dte, base_sv_dte, haciendaws_fe_sv_dte |
| `hacienda_fse_sv_dte` | base, hacienda_sv_dte, base_sv_dte, haciendaws_fe_sv_dte |
| `hacienda_invalidadion_sv_dte` | base, hacienda_sv_dte, base_sv_dte, haciendaws_fe_sv_dte |
| `hacienda_payment_terms_sv_dte` | haciendaws_fe_sv_dte, sv_dte, base |
| `mh_anexos_sv_dte` | base, invoice_sv_dte, account, phone_validation, l10n_latam_base, haciendaws_fe_sv_dte, hacienda_invalidadion_sv_dte |
| `dte_import_sv_dte` | account, product, contacts, uom |
| `journal_sequence_sv_dte` | account |
| `partidas_sv_dte` | account |
| `quedan_sv_dte` | account |
| `reportes_ventas_sv_dte` | base, account, sale, invoice_sv_dte |
| `purchase_sv_dte` | purchase, account, sv_dte, hacienda_contingencia_sv_dte, invoice_sv_dte, mh_anexos_sv_dte |
| `hr_retenciones_sv_dte` | hr, **hr_payroll**, hr_attendance |
| `rrhh_base_sv_dte` | hr_retenciones_sv_dte, **hr_payroll** |
| `hr_asignaciones_sv_dte` | web, base, hr, **hr_payroll**, hr_retenciones_sv_dte, resource |
| `planilla_unica_sv_dte` | base, hr, **hr_payroll**, rrhh_base_sv_dte, hr_asignaciones_sv_dte, hr_retenciones_sv_dte |
| `despacho_sv_dte` | web, dpto_sv_dte, hacienda_sv_dte, stock, **stock_barcode**, sale, fleet, hr, account, mail |
| `shopify_fast_connector` | sale_management, account, stock, product, contacts, mail |

> Las dependencias en **negrita** son de **Odoo Enterprise**.

---

## Resumen rápido

- **Solo facturación DTE** → Odoo **Community** + app **Contabilidad** + los módulos
  de la cadena DTE (sección 4.1). Suficiente para emitir y enviar DTE a Hacienda.
- **+ RRHH / Planilla** → requiere **Odoo Enterprise** (`hr_payroll`).
- **+ Despacho** → requiere **Odoo Enterprise** (`stock_barcode`).
