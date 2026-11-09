/**
 * Codici di avviamento postale dei comuni, per proporre il CAP del dichiarante quando si sceglie il comune
 * di residenza. I comuni con più CAP (le città maggiori) restituiscono l'elenco completo: la scelta spetta
 * al tecnico in base all'indirizzo.
 */
import { CAP_INCORPORATI } from './dati/cap.generated';

let indice: Map<string, string[]> | undefined;

function carica(): Map<string, string[]> {
  if (!indice) {
    indice = new Map();
    for (const riga of CAP_INCORPORATI.split('\n')) {
      const [codice, elenco] = riga.split('|');
      if (codice && elenco) indice.set(codice, elenco.split(','));
    }
  }
  return indice;
}

/** CAP del comune con il codice catastale indicato (es. A470 → ['46041']); vuoto se non noto. */
export function capDelComune(codiceCatastale: string | undefined): string[] {
  if (!codiceCatastale) return [];
  return carica().get(codiceCatastale.trim().toUpperCase()) ?? [];
}
