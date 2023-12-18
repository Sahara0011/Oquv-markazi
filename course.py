from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.start import contact
from keyboards.inline.course_kb import courses, registration
from loader import dp
from states.user_registration import UserRegistration

informations = {}


@dp.message_handler(text='📚 Kurslarimiz')
async def kurs_keyboard(message: types.Message):
    photo = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLSPHOgFtj-PowgsW4mf4PeuS-h0vz2x9a0Q&usqp=CAU'
    await message.answer_photo(photo=photo, caption='Kurslarimiz haqida malumot...',
                               reply_markup=courses)
    await UserRegistration.course.set()


@dp.callback_query_handler(state=UserRegistration.course)
async def starter_keyboard(call: types.CallbackQuery, state: FSMContext):
    c_data = call.data
    if c_data == 'starter':
        photo_s = 'https://cdn.akamai.steamstatic.com/steam/bundles/23696/ie7nmltk4hwnlt38/header_586x192.jpg?t=1637329124'
        await call.message.answer_photo(photo=photo_s, caption='Starter kursi 3 oy davom etadi...',
                                        reply_markup=registration)
        await state.update_data(course='Starter kursi')

    elif c_data == 'frontend':
        photo_s = 'https://tolustar.com/wp-content/uploads/2020/02/Front-end-Development.jpeg'
        await call.message.answer_photo(photo=photo_s, caption='frontend kursi 3 oy davom etadi',
                                        reply_markup=registration)
        await state.update_data(course='Frontend kursi')

    elif c_data == 'backend':
        photo_s = 'https://images.shiksha.com/mediadata/ugcDocuments/images/wordpressImages/2021_12_backend-development-1-1.jpg'
        await call.message.answer_photo(photo=photo_s, caption='backend kursi 9 oy davom etadi',
                                        reply_markup=registration)
        await state.update_data(course='Backend kursi')

    elif c_data == 'grafik':
        photo_s = 'https://bilgi.uz/upload/resize_cache/iblock/096/2q5y98olf0phywe39untsyybxq2fekil/0_350_2/grafk.jpg'
        await call.message.answer_photo(photo=photo_s, caption='grafik dizayn kursi 6 oy davom etadi',
                                        reply_markup=registration)
        await state.update_data(course='Grafik Dizayn kursi')

    elif c_data == '3d':
        photo_s = 'https://interyernew.ru/wp-content/uploads/2019/08/2586.jpg'
        await call.message.answer_photo(photo=photo_s, caption='3D dizayn kursi 6 oy davom etadi',
                                        reply_markup=registration)
        await state.update_data(course='3D dizayn kursi')

    elif c_data == 'beck_to_main':
        await call.message.answer('Menyuni tanglang:', reply_markup=starter_keyboard)
        await state.finish()


    elif c_data == 'registration':
        await call.message.answer('Ismingizni kiriting')
        await UserRegistration.next()


    elif c_data == 'back_to_course':
        photo_s = 'https://marsit.uz/images/tild6362-6431-4430-b636-6635 5313631___3_.jpg'
        await call.message.answer_photo(photo=photo_s, caption='Kurslarimiz haqida kursi 6 oy davom etadi',
                                        reply_markup=registration)
        await UserRegistration.course.set()


@dp.message_handler(state=UserRegistration.name)
async def get_name(message: types.Message, state: FSMContext):
    ism = message.text
    await state.update_data(name=ism)
    await message.answer('Telefon raqamingizni kiriting', reply_markup=contact)
    await UserRegistration.next()


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=UserRegistration.phone)
async def get_contact(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await message.answer(f'Sizning telefon raqamingiz: {phone_number}')
    await state.update_data(phone=phone_number)
    data = await state.get_data()
    informations.update(data)
    informations.update({'user_id': message.from_user.id})
    await message.answer('Sizning ma\'lumotlaringiz qabul qilindi. Tez orada siz bilan bog\'lanamiz!\n'
                         f'Sizning ma\'lumotlaringiz:{informations}',

                         reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
