const path = require('path')
const express = require('express')
const bodyParser = require('body-parser')
const mongoose = require('mongoose')

const app = express()
const mainDirectory = path.join(__dirname,'../public')
app.use(express.static(path.join(__dirname, '../views')))
app.use(express.static(mainDirectory))
app.set('view engine','hbs')
app.use(bodyParser.urlencoded({extended:true}))

const MongoClient = require('mongodb').MongoClient;

mongoose.connect('mongodb+srv://danilopc2:danilo11@cluster0-m9cda.mongodb.net/textos_classificar',{ 
    useNewUrlParser: true, 
    useCreateIndex:true, 
    useUnifiedTopology: true
})

const textClassModel =  mongoose.model('textos', {
    'texto_bruto' : {
        type: String
    },
    'classe' : {
        type: String
    }
})

// APP
app.get('', (req,res, next) => {
    textClassModel.countDocuments({'classe':'Indefinida'})
    .then((numero) => {
        res.render('index', {
            numero_textos_sem_classe:numero
        })}
    ).catch((err) => {
        console.log(err)
    })
})

app.get('/classificar_texto', (req,res) => {
    textClassModel.find({'classe':'Indefinida'}).then((dataTexto) => {
        var dicionario = dataTexto[0]
        var texto_bruto = dicionario.texto_bruto
        var textoId = dicionario._id
        res.render('classificar_texto', {
            texto_bruto:texto_bruto,
            textoId:textoId,
            classes_disponiveis:[{
                classe_id:'-1',
                classe_nome:'talvez'
            },
            {
                classe_id:'0',
                classe_nome:'impertinente'
            },
            {
                classe_id:'1',
                classe_nome:'pertinente'
            }
        ]
        })
    }).catch((err) => {
        console.log(err)
    })
})

app.post('/classificar', (req,res) => {
    var classe_texto = req.body.classe_texto
    var textoId = req.body.textoId
    textClassModel.findOneAndUpdate({'_id':textoId},{'classe':classe_texto}).then(() => {
        res.redirect('/')
    })
})

app.listen(3333, () => {
    console.log('Servidor no ar')
})