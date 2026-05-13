import * as v from "valibot";

const pattern = /^[А-ЯЁа-яё][А-ЯЁа-яёIV\-.,'()\s]*[А-ЯЁа-яё]$|^[А-ЯЁа-яё]$/;

export const empty = v.object({});

export const schemaResume = v.object({
  surname: v.pipe(
    v.string(),
    v.regex(pattern, "Недопустимые символы!"),
    v.toUpperCase(),
  ),
  firstname: v.pipe(
    v.string(),
    v.regex(pattern, "Недопустимые символы!"),
    v.toUpperCase(),
  ),
  patronymic: v.pipe(
    v.string(),
    v.check(
      (value) => value === "" || pattern.test(value),
      "Недопустимые символы!",
    ),
    v.toUpperCase(),
  ),
  birthday: v.pipe(
    v.string(),
    v.toDate(),
    v.maxValue(new Date(), "Дата находится в будущем!"),
    v.minValue(new Date(1900, 0, 1), "Дата слишком старая!"),
  ),
  birthplace: v.string(),
  citizenship: v.string(),
  dual: v.string(),
  snils: v.pipe(
    v.string(),
    v.check(
      (value) => value === "" || /^\d{11}$/.test(value),
      "Должно быть 11 цифр!",
    ),
  ),
  inn: v.pipe(
    v.string(),
    v.check(
      (value) => value === "" || /^\d{12}$/.test(value),
      "Должно быть 12 цифр!",
    ),
  ),
  marital: v.string(),
  addition: v.string(),
});

export const parserResume = v.parser(schemaResume);

export const schemaDoc = v.object({
  view: v.pipe(
    v.string(),
    v.union([
      v.literal("Паспорт"),
      v.literal("Иностранный паспорт"),
      v.literal("Другое"),
    ]),
  ),
  series: v.string(),
  digits: v.pipe(v.string(), v.regex(/^\d{1,12}$/, "Недопустимые символы!")),
  agency: v.string(),
  issue: v.pipe(
    v.string(),
    v.toDate(),
    v.maxValue(new Date(), "Дата находится в будущем!"),
    v.minValue(new Date(1900, 0, 1), "Дата слишком старая!"),
  ),
});

export const schemaWork = v.object({
  starts: v.pipe(
    v.string(),
    v.toDate(),
    v.minValue(new Date(1900, 0, 1), "Дата слишком старая!"),
  ),
  finished: v.pipe(
    v.string(),
    v.toDate(),
    v.minValue(new Date(1900, 0, 1), "Дата слишком старая!"),
  ),
  workplace: v.string(),
  position: v.string(),
  address: v.string(),
  reason: v.string(),
});

export const fallbackParser = (schema: any) => {
  return v.parser(
    v.object(
      Object.fromEntries(
        Object.keys(schema.entries).map((name) => [
          name,
          v.fallback(v.string(), ""),
        ]),
      ),
    ),
  );
};
