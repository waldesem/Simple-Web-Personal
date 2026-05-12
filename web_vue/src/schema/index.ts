import * as v from "valibot";

const pattern = /^[А-ЯЁа-яё][А-ЯЁа-яёIV\-.,'()\s]*[А-ЯЁа-яё]$|^[А-ЯЁа-яё]$/;

export const empty = v.object({});

export const schemaFallbackResume = v.object({
  surname: v.fallback(v.string(), ""),
  firstname: v.fallback(v.string(), ""),
  patronymic: v.fallback(v.string(), ""),
  birthday: v.fallback(v.string(), ""),
  birthplace: v.fallback(v.string(), ""),
  citizenship: v.fallback(v.string(), ""),
  dual: v.fallback(v.string(), ""),
  snils: v.fallback(v.string(), ""),
  inn: v.fallback(v.string(), ""),
  marital: v.fallback(v.string(), ""),
  addition: v.fallback(v.string(), ""),
});

export const fallbackResume = v.parser(schemaFallbackResume);

export const schemaResume = v.object({
  surname: v.pipe(
    v.string(),
    v.nonEmpty("Обязательное поле!"),
    v.regex(pattern, "Недопустимые символы!"),
    v.maxLength(255, "Не более 255 символов!"),
    v.toUpperCase(),
  ),
  firstname: v.pipe(
    v.string(),
    v.nonEmpty("Обязательное поле!"),
    v.regex(pattern, "Недопустимые символы!"),
    v.maxLength(255, "Не более 255 символов!"),
    v.toUpperCase(),
  ),
  patronymic: v.pipe(
    v.string(),
    v.check(
      (value) => value === "" || pattern.test(value),
      "Недопустимые символы!",
    ),
    v.maxLength(255, "Не более 255 символов!"),
    v.toUpperCase(),
  ),
  birthday: v.pipe(
    v.string(),
    v.nonEmpty("Обязательное поле!"),
    v.toDate(),
    v.maxValue(new Date(), "Дата находится в будущем!"),
    v.minValue(new Date(1900, 0, 1), "Дата слишком старая!"),
  ),
  birthplace: v.pipe(v.string(), v.maxLength(255, "Не более 255 символов!")),
  citizenship: v.pipe(v.string(), v.maxLength(255, "Не более 255 символов!")),
  dual: v.pipe(v.string(), v.maxLength(255, "Не более 255 символов!")),
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
  marital: v.pipe(v.string(), v.maxLength(255, "Не более 255 символов!")),
  addition: v.pipe(v.string(), v.maxLength(4096, "Не более 4096 символов!")),
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
  series: v.pipe(v.string(), v.maxLength(255)),
  digits: v.pipe(
    v.string(),
    v.nonEmpty("Обязательное поле!"),
    v.regex(/^\d{1,12}$/, "Недопустимые символы!"),
  ),
  agency: v.pipe(v.string(), v.maxLength(255)),
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
    v.nonEmpty("Обязательное поле!"),
    v.toDate(),
    v.minValue(new Date(1900, 0, 1), "Дата слишком старая!"),
  ),
  workplace: v.pipe(
    v.string(),
    v.nonEmpty("Обязательное поле!"),
    v.maxLength(255, "Не более 255 символов!"),
  ),
  position: v.pipe(
    v.string(),
    v.nonEmpty("Обязательное поле!"),
    v.maxLength(255, "Не более 255 символов!"),
  ),
  address: v.pipe(v.string(), v.maxLength(255, "Не более 255 символов!")),
  reason: v.pipe(v.string(), v.maxLength(4096, "Не более 4096 символов!")),
});
